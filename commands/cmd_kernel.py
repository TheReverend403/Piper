import ujson as json

import re
import requests
from lib.command import Command
from lib.utils import telegram_escape


class KernelCommand(Command):
    name = 'kernel'
    aliases = ['linux']
    description = 'Shows current Linux kernel versions.'

    def run(self, message, args):
        response = None
        try:
            self.bot.telegram.send_chat_action(message.chat.id, 'typing')
            response = requests.get('https://www.kernel.org/releases.json')
        except requests.exceptions.RequestException as ex:
            self.reply(message, 'Error: {0}'.format(ex.strerror))
            self._logger.exception(ex)
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
                    telegram_escape(branch['version']),
                    telegram_escape(branch['moniker']),
                    telegram_escape(branch['changelog'] if branch['changelog'] else branch['gitweb']),
                    telegram_escape(branch['source'] if branch['source'] else branch['gitweb'])))

        if not versions and args:
            self.reply(message, 'No kernel versions found for {0}!'.format(args[0]))
            return

        reply = '\n'.join(versions)
        self.reply(message, reply, parse_mode='HTML')
