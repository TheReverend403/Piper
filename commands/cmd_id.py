from lib.command import Command


class IdCommand(Command):
    name = 'id'
    description = 'Returns your user ID, or the ID of the current chat when -c is passed as an argument.'

    def run(self, message, args):
        reply = 'Your Telegram ID is {0}'.format(message.from_user.id)
        if self.is_admin(message.from_user):
            reply += ' and you are a bot admin.'
        if '-c' in args:
            reply = 'This chat\'s ID is {0}'.format(message.chat.id)
        self.reply(message, reply)
