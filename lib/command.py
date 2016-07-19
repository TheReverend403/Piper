import logging

from lib.database import Database


class Command(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.logger = logging.getLogger('pyper.command.' + self.name)
        if self._has_database():
            self.database = Database('data/{0}.json'.format(self.name))

    def reply(self, message, reply, **kwargs):
        if 'disable_web_page_preview' not in kwargs:
            kwargs['disable_web_page_preview'] = True
        self.bot.telegram.reply_to(message, reply, **kwargs)

    def _has_database(self):
        return hasattr(self, 'has_database') and self.has_database
