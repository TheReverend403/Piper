import logging


class Command(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.logger = logging.getLogger('pyper.command.' + self.name)

    def reply(self, message, reply, **kwargs):
        if 'disable_web_page_preview' not in kwargs:
            kwargs['disable_web_page_preview'] = True
        self.bot.telegram.reply_to(message, reply, **kwargs)
