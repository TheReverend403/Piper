import logging

from lib.database import Database
from lib.utils import emojify


class Command(object):
    def __init__(self, bot, config):
        self.bot = bot
        self._config = config
        self._logger = logging.getLogger('pyper.command.' + self.name)
        if self._has_database():
            self._database = Database('data/{0}.json'.format(self.name))
        self.aliases = self._get_aliases()

    def reply(self, message, reply, **kwargs):
        if 'disable_web_page_preview' not in kwargs:
            kwargs['disable_web_page_preview'] = True

        if 'emojify' in kwargs and kwargs['emojify']:
            reply = emojify(reply)
            del kwargs['emojify']

        self.bot.telegram.reply_to(message, reply, **kwargs)

    def _has_database(self):
        return hasattr(self, 'has_database') and self.has_database

    def _get_aliases(self):
        return self.aliases if hasattr(self, 'aliases') else []
