from lib.command import Command
from datetime import timedelta
from uptime import uptime


class UptimeCommand(Command):
    name = 'uptime'
    description = 'Prints the current system uptime.'

    def run(self, message, args):
        uptime_seconds = int(uptime())
        uptime_string = str(timedelta(seconds=uptime_seconds))
        self.reply(message, uptime_string)
