import logging

import os
import sys

from lib.database import Database
from lib.utils import emojify


class Command(object):
    def __init__(self, bot, config):
        self.bot = bot
        self._config = config

        self.name = self.__get_name()
        self.description = self.__get_description()
        if not self.name or not self.description:
            self._logger.error('Command is missing required attribute \'name\' or \'description\''.format(__name__))
            del self
            return

        self._logger = logging.getLogger('pyper.command.' + self.name)

        if self.__has_database():
            database_path = os.path.realpath('{0}/../../data/{1}.json'.format(os.path.realpath(sys.argv[0]), self.name))
            self._logger.debug('Storing database for %s at %s', self.name, database_path)
            self._database = Database(database_path)

        self.aliases = self.__get_aliases()
        self.admin_only = self.__is_admin_only()
        self._logger.debug('Loaded command %s.', self.name)

    def authorized(self, user):
        if self.admin_only:
            return self.bot.is_admin(user)
        return True

    def reply(self, message, reply, **kwargs):
        if 'disable_web_page_preview' not in kwargs:
            kwargs['disable_web_page_preview'] = True

        if 'emojify' in kwargs and kwargs['emojify']:
            reply = emojify(reply)
            del kwargs['emojify']

        if type(reply) is list:
            reply = ' '.join(reply)

        self.bot.telegram.reply_to(message, reply, **kwargs)

    def __has_database(self):
        if hasattr(self, 'has_database'):
            return self.has_database
        return False

    def __is_admin_only(self):
        if hasattr(self, 'admin_only'):
            return self.admin_only
        return False

    def __get_name(self):
        if hasattr(self, 'name'):
            return self.name
        return None

    def __get_description(self):
        if hasattr(self, 'description'):
            return self.description
        return None

    def __get_aliases(self):
        return self.aliases if hasattr(self, 'aliases') else []
