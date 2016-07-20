from lib.command import Command


class EchoCommand(Command):
    name = 'echo'
    description = 'Replies with whatever input you send.'

    def run(self, message, args):
        if args:
            self.reply(message, ' '.join(args), emojify=True)
        else:
            self.reply(message, 'Please supply some args!')
