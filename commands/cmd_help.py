from lib.command import Command
from lib.utils import telegram_escape, emojify


class HelpCommand(Command):
    name = 'help'
    aliases = ['start']
    description = 'Lists all bot commands and their descriptions.'

    def run(self, message, args):
        reply = emojify('Hi! I\'m {0} and these are my commands.\n\n'.format(
            self.bot.telegram.get_me().username))
        for command in self.bot.commands.values():
            if not command.authorized(message.from_user):
                continue
            reply += '/{0} - <b>{1}</b>'.format(telegram_escape(command.name), telegram_escape(command.description))
            if command.aliases:
                reply += ' <b>(</b>Aliases: /{0}<b>)</b>'.format(telegram_escape(', /'.join(command.aliases)))
            if command.admin_only:
                reply += emojify(' (:lock:)')
            reply += '\n'

        reply += '\nYou can find my source code at https://github.com/TheReverend403/Pyper'
        self.reply(message, reply, parse_mode='HTML')
