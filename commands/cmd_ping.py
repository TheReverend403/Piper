import platform
import subprocess

import re

from lib.command import Command


class PingCommand(Command):
    name = 'ping'
    aliases = ['isup']
    description = 'Checks whether a given host is up.'

    def run(self, message, args):
        if not args:
            self.reply(message, 'Please supply a host to check.')
            return

        host = args[0].strip()
        self.bot.telegram.send_chat_action(message.chat.id, 'typing')
        try:
            ping = str(subprocess.check_output(
                ['ping', '-n' if platform.system().lower() == 'windows' else '-c', '1', host], stderr=subprocess.STDOUT,
                timeout=5))
        except subprocess.TimeoutExpired as ex:
            self.reply(message, '{0} looks down from here. (Timed out after {1} seconds)'.format(host, ex.timeout),
                       disable_web_page_preview=True)
            return
        except subprocess.CalledProcessError as ex:
            if 'unknown host' in str(ex.output):
                self.reply(message, '{0} doesn\'t seem to be a resolvable host!'.format(host),
                           disable_web_page_preview=True)
            return

        ip_match = re.match('.*\((.+)\):.*', ping)
        time_match = re.match('.*time=(\d+)', ping)
        time = time_match.group(1).strip() if time_match and time_match.groups() else 0
        ip = ip_match.group(1).strip() if ip_match and ip_match.groups() else None

        self.reply(message, '{0} ({1}) is up ({2} ms).'.format(host, ip or host, time), disable_web_page_preview=True)
