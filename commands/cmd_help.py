from lib.command import Command


class HelpCommand(Command):
    name = 'help'
    aliases = ['start']
    description = 'Lists all bot commands and their descriptions.'

    def run(self, message, args):
        reply = 'Hi! I\'m {0} and these are my commands: \n\n'.format(self.bot.telegram.get_me().username)
        for command in self.bot.commands.values():
            reply += '/{0} - {1}'.format(command.name, command.description)
            if hasattr(command, 'aliases'):
                reply += ' (Aliases: /{0})'.format(', '.join(command.aliases))
            reply += '\n'

        reply += '\nYou can find my source code at https://github.com/TheReverend403/Piper'
        self.reply(message, reply)
