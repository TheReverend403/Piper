import logging

import os
import sys

from lib.database import Database
from lib.utils import emojify


class Command(object):
    def __init__(self, bot, config):
        self.bot = bot
        self._config = config
        self._logger = logging.getLogger('pyper.command.' + self.name)
        self.name = self.__get_name()
        self.description = self.__get_description()
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

        try:
            if kwargs['emojify']:
                reply = emojify(reply)
                del kwargs['emojify']
        except KeyError:
            pass

        if type(reply) is list:
            reply = ' '.join(reply)

        self.bot.telegram.reply_to(message, reply, **kwargs)

    def __is_admin_only(self):
        try:
            return self.admin_only
        except AttributeError:
            return False

    def __get_name(self):
        try:
            return self.name
        except AttributeError:
            raise

    def __get_description(self):
        try:
            return self.description
        except AttributeError:
            raise

    def __get_aliases(self):
        try:
            return self.aliases
        except AttributeError:
            return []
