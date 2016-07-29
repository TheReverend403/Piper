import logging
import ujson as json

import os
import requests
import telebot

from lib import importdir
from lib.command import Command
from lib.database import Database
from lib.utils import user_to_string, chat_to_string


class Bot(object):
    def __init__(self, config):
        self._config = config
        self.telegram = telebot.TeleBot(config.get('bot', 'key'), skip_pending=True)
        telebot.logger.setLevel(logging.WARNING)
        self._logger = logging.getLogger('pyper')
        self._database = Database('data/pyper.json')
        self.admins = []
        self._init_config()
        self.commands = {}
        self._init_commands()
        self.telegram.set_update_listener(self._handle_messages)

    def _init_config(self):
        self._logger.info('Loading config.')
        try:
            if self._config.has_option('bot', 'admins'):
                self.admins = json.loads(self._config.get('bot', 'admins'))
        except ValueError as ex:
            self._logger.exception(ex)
        self._logger.info('Bot admin IDs: %s', self.admins)

    def _init_commands(self):
        self._logger.info('Loading commands.')
        importdir.do('commands', globals())
        if self._config.has_option('bot', 'extra_commands_dir'):
            extra_commands_dir = self._config.get('bot', 'extra_commands_dir')
            if extra_commands_dir and os.path.exists(extra_commands_dir):
                self._logger.info('Added %s to command load path.', extra_commands_dir)
                importdir.do(extra_commands_dir, globals())

        disabled_commands = []
        try:
            if self._config.has_option('bot', 'disabled_commands'):
                disabled_commands = json.loads(self._config.get('bot', 'disabled_commands'))
        except ValueError as ex:
            self._logger.exception(ex)

        for command in Command.__subclasses__():
            if command.name not in disabled_commands:
                self._enable_command(command)
            else:
                del command

        self._logger.info('Enabled commands: %s.', list(self.commands.keys()))
        if disabled_commands:
            self._logger.info('Disabled commands: %s.', disabled_commands)

    def _handle_messages(self, messages):
        for message in messages:
            self._logger.debug(message)
            if message.new_chat_member:
                if self.is_me(message.new_chat_member):
                    self._logger.info('Joined chat %s', chat_to_string(message.chat))
                    continue
            if message.left_chat_member:
                if self.is_me(message.left_chat_member):
                    self._logger.info('Left chat %s', chat_to_string(message.chat))
                    continue

            if not message.text or not message.from_user:
                continue
            user = message.from_user
            if self._database.get_user_value(message.from_user, 'ignored'):
                self._logger.info('Ignoring message %s because user %s is ignored.', message, user_to_string(user))
                continue

            if message.text.startswith('/'):
                message_text = message.text.strip('/')
                if not message_text:
                    continue

                command_split = message_text.split()
                command_trigger, __, bot_name = ''.join(command_split[:1]).lower().partition('@')
                if bot_name and bot_name != self.telegram.get_me().username:
                    continue
                args = list(filter(bool, command_split[1:]))

                for command in self.commands:
                    command = self.commands[command]
                    if command_trigger == command.name or command_trigger in command.aliases:
                        log_msg = 'Command \'{0}\' with args {1} invoked by user {2}'.format(command.name, args,
                                                                                             user_to_string(user))
                        if message.chat.type != 'private':
                            log_msg += ' from chat {0}'.format(chat_to_string(message.chat))

                        if command.authorized(user):
                            self._logger.info(log_msg)
                            command.run(message, args)
                        else:
                            log_msg += ', but access was denied.'
                            self._logger.info(log_msg)
                            command.reply(message, 'You are not authorized to use that command!')

    def poll(self):
        try:
            self._logger.info('Started polling.')
            self.telegram.polling(none_stop=True, timeout=5)
        except requests.exceptions.RequestException as ex:
            self._logger.exception(ex)
            self._logger.warn('Restarting polling due to RequestException.')
            self.telegram.stop_polling()
            self.poll()

    def _enable_command(self, command):
        if command not in self.commands.values():
            config = dict(self._config.items(command.name)) if self._config.has_section(command.name) else None
            command = command(self, config)
            self.commands[command.name] = command

    def ignore(self, user):
        self._logger.info('Ignored user %s', user_to_string(user))
        self._database.set_user_value(user, 'ignored', True)

    def unignore(self, user):
        self._logger.info('Unignored user %s', user_to_string(user))
        self._database.set_user_value(user, 'ignored', False)

    def is_me(self, user):
        return user.id == self.telegram.get_me().id

    def is_admin(self, user):
        return user.id in self.admins
