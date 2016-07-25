import logging
import ujson as json

import os
import requests
import telebot

from lib import importdir
from lib.command import Command
from lib.database import Database
from lib.utils import user_to_string


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

        self._logger.info('Enabled commands: [%s].', ', '.join(self.commands.keys()))
        if disabled_commands:
            self._logger.info('Disabled commands: [%s].', ', '.join(disabled_commands))

    def _handle_messages(self, messages):
        for message in messages:
            self._logger.debug(message)

            if not message.text or not message.from_user:
                continue
            user = message.from_user
            if self._database.get_user_value(message.from_user, 'ignored'):
                self._logger.info('Ignoring message %s because user %s: %s is ignored.',
                                  message, user.id, user_to_string(user))
                continue

            if message.text.startswith('/'):
                message_text = message.text.strip('/')
                if not message_text:
                    return

                command_split = message_text.split()
                command_trigger, _, _ = ''.join(command_split[:1]).lower().partition('@')
                args = list(filter(bool, command_split[1:]))

                for command in self.commands:
                    command = self.commands[command]
                    if command_trigger == command.name or command_trigger in command.aliases:
                        self._logger.info('Command \'%s\' with args %s invoked by user %s: %s',
                                          command.name, args, user.id, user_to_string(user))
                        if command.authorized(user):
                            command.run(message, args)
                        else:
                            command.reply(message, 'You are not authorized to use that command!')

    def poll(self):
        try:
            self.telegram.polling(none_stop=True, timeout=3)
        except requests.exceptions.ConnectionError as ex:
            self._logger.exception(ex)
            self.telegram.stop_polling()
            self.poll()
        except KeyboardInterrupt:
            self.telegram.stop_polling()

    def _enable_command(self, command):
        if command not in self.commands.values():
            config = dict(self._config.items(command.name)) if self._config.has_section(command.name) else None
            command = command(self, config)
            self.commands[command.name] = command

    def ignore(self, user):
        self._database.set_user_value(user, 'ignored', True)

    def unignore(self, user):
        self._database.set_user_value(user, 'ignored', False)

    def is_me(self, user):
        return user.id == self.telegram.get_me().id

    def is_admin(self, user):
        return user.id in self.admins
