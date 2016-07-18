class Command(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    def reply(self, message, reply, **kwargs):
        self.bot.telegram.reply_to(message, reply, **kwargs)
