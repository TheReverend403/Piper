from lib.command import Command

from bs4 import BeautifulSoup
import requests


class WhatTheCommitCommand(Command):
    name = 'whatthecommit'
    aliases = ['wtc']
    description = 'Gets a random commit message from http://whatthecommit.com'

    def run(self, message, args):
        request = None
        try:
            request = requests.get('http://whatthecommit.com')
        except requests.exceptions.RequestException as ex:
            self.reply(message, 'Error: {0}'.format(ex.strerror), disable_web_page_preview=True)
            self.bot.logger.error(ex)
            return
        finally:
            if request is not None:
                request.close()
        html = request.text
        parsed_html = BeautifulSoup(html, 'html.parser')
        commit_message = parsed_html.body.find('div', id='content').find('p').text
        self.reply(message, commit_message, disable_web_page_preview=True)
