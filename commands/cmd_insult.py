from lib.command import Command
from lib.utils import escape_telegram_html

from bs4 import BeautifulSoup
import requests


class InsultCommand(Command):
    name = 'insult'
    aliases = ['abuse']
    description = 'Gets a random insult from http://www.insultgenerator.org'

    def run(self, message, args):
        response = None
        try:
            response = requests.get('http://www.insultgenerator.org')
        except requests.exceptions.RequestException as ex:
            self.reply(message, 'Error: {0}'.format(ex.strerror))
            self.logger.exception(ex)
            return
        finally:
            if response is not None:
                response.close()

        html = response.text
        parsed_html = BeautifulSoup(html, 'html.parser')
        insult_html = parsed_html.body.find('div', {'class': 'wrap'})
        insult = escape_telegram_html(insult_html.text.strip())
        self.reply(message, insult, parse_mode='HTML')
