import requests
from bs4 import BeautifulSoup
from lib.command import Command
from lib.utils import telegram_escape


class WhatTheCommitCommand(Command):
    name = 'whatthecommit'
    aliases = ['wtc']
    description = 'Gets a random commit message from whatthecommit.com'

    def run(self, message, args):
        response = None
        try:
            response = requests.get('http://whatthecommit.com')
        except requests.exceptions.RequestException as ex:
            self.reply(message, 'Error: {0}'.format(ex.strerror))
            self._logger.exception(ex)
            return
        finally:
            if response is not None:
                response.close()

        html = response.text
        parsed_html = BeautifulSoup(html, 'html.parser')
        commit_message = parsed_html.body.find('div', id='content').find('p').text
        reply = '<pre>git commit -am "{0}"</pre>'.format(telegram_escape(commit_message.strip()))
        self.reply(message, reply, parse_mode='HTML')
