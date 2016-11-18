import requests
from lxml import html

from lib.command import Command


class InsultCommand(Command):
    name = 'insult'
    aliases = ['abuse']
    description = 'Gets a random insult from http://www.insultgenerator.org'

    def run(self, message, args):
        try:
            self.bot.telegram.send_chat_action(message.chat.id, 'typing')
            response = requests.get('http://www.insultgenerator.org')
        except requests.exceptions.RequestException as ex:
            self._logger.exception(ex)
            self.reply(message, 'Error: {0}'.format(ex.strerror))
        else:
            doc = html.fromstring(response.text)
            insult = ''.join(doc.xpath('//div[@class="wrap"]/text()')).strip()
            self.reply(message, insult)
