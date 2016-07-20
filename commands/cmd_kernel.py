import json

import re
import requests
from lib.command import Command
from lib.utils import escape_telegram_html


class KernelCommand(Command):
    name = 'kernel'
    aliases = ['linux']
    description = 'Shows current Linux kernel versions.'

    def run(self, message, args):
        response = None
        try:
            response = requests.get('https://www.kernel.org/releases.json')
        except requests.exceptions.RequestException as ex:
            self.reply(message, 'Error: {0}'.format(ex.strerror))
            self.logger.exception(ex)
            return
        finally:
            if response is not None:
                response.close()

        parsed = json.loads(response.text)
        versions = []

        regex = False
        if args:
            regex = re.compile(r'^.*' + re.escape(args[0]) + r'.*$', re.I)

        for branch in parsed['releases']:
            if regex:
                if not regex.match(branch['moniker']) and not regex.match(branch['version']):
                    continue
            versions.append(
                '<b>{0}</b> ({1}|<a href="{2}">changelog</a>|<a href="{3}">source</a>)'.format(
                    escape_telegram_html(branch['version']),
                    escape_telegram_html(branch['moniker']),
                    escape_telegram_html(branch['changelog'] if branch['changelog'] else branch['gitweb']),
                    escape_telegram_html(branch['source'] if branch['source'] else branch['gitweb'])))

        reply = '\n'.join(versions)
        self.reply(message, reply, parse_mode='HTML')
