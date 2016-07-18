import platform

from lib.command import Command


class BotsCommand(Command):
    name = 'bots'
    description = 'Report in!'

    def run(self, message, args):
        self.reply(message, 'Reporting in! [Python {0}]'.format(platform.python_version()))
