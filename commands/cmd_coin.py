from lib.command import Command
import random


class EchoCommand(Command):
    name = 'coin'
    description = 'Flip a coin.'

    def run(self, message, args):
        self.reply(message, random.choice(['Heads', 'Tails']))
