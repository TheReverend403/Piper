import requests
from lxml import html
from lib.command import Command
from lib.utils import telegram_escape


class WhatTheCommitCommand(Command):
    name = 'whatthecommit'
    aliases = ['wtc']
    description = 'Gets a random commit message from whatthecommit.com'

    def run(self, message, args):
        try:
            self.bot.telegram.send_chat_action(message.chat.id, 'typing')
            response = requests.get('http://whatthecommit.com/index.txt')
        except requests.exceptions.RequestException as ex:
            self._logger.exception(ex)
            self.reply(message, 'Error: {0}'.format(ex.strerror))
        else:
            commit_message = response.text.strip()
            reply = '<pre>git commit -am "{0}"</pre>'.format(telegram_escape(commit_message))
            self.reply(message, reply, parse_mode='HTML')
