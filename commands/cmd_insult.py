import requests
from bs4 import BeautifulSoup

from lib.command import Command


class InsultCommand(Command):
    name = 'insult'
    aliases = ['abuse']
    description = 'Gets a random insult from http://www.insultgenerator.org'

    def run(self, message, args):
        response = None
        try:
            self.bot.telegram.send_chat_action(message.chat.id, 'typing')
            response = requests.get('http://www.insultgenerator.org')
        except requests.exceptions.RequestException as ex:
            self.reply(message, 'Error: {0}'.format(ex.strerror))
            self._logger.exception(ex)
            return
        finally:
            if response is not None:
                response.close()

        html = response.text
        parsed_html = BeautifulSoup(html, 'html.parser')
        insult_html = parsed_html.body.find('div', {'class': 'wrap'})
        insult = insult_html.text.strip()
        self.reply(message, insult)
