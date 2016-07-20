import pylast
from lib.command import Command
from lib.utils import telegram_escape

SET_STRINGS = [
    '-s', '-set', '--set', 'set'
]


class LastFMCommand(Command):
    name = 'lastfm'
    aliases = ['np', 'nowplaying']
    description = 'Post your currently playing song.'
    has_database = True

    def __init__(self, bot, config):
        super().__init__(bot, config)
        if not self.config or 'api_key' not in self.config:
            self.logger.error('last.fm API key is not configured.')
            self.config = None
            return
        else:
            try:
                self.__network = pylast.LastFMNetwork(api_key=self.config['api_key'])
            except pylast.NetworkError as ex:
                self.logger.exception(ex)
                self.config = None
                return

    def run(self, message, args):
        if not self.config:
            self.reply(message, 'last.fm command is not configured!')
            return

        user = message.from_user
        if args and args[0] in SET_STRINGS:
            if len(args) == 1:
                self.reply(message, 'Please provide a username. (/np -s <username>)')
                return
            username = args[1].strip()
            try:
                self.database.set_user_value(user, 'lastfm',
                                             self.__network.get_user(username).get_name(properly_capitalized=True))
                self.reply(message, 'last.fm username set.')
                return
            except pylast.WSError:
                self.reply(message, 'No such last.fm user. Are you trying to trick me? :^)')
                return

        username = self.database.get_user_value(user, 'lastfm')
        if not username:
            self.reply(message, 'You have no last.fm username set. Please set one with /np -s <username>')
            return

        lastfm_user = self.__network.get_user(username)
        current_track = lastfm_user.get_now_playing()
        if not current_track:
            reply = '<a href="http://www.last.fm/user/{0}">{0}</a> is not listening to anything right now.'.format(
                telegram_escape(username))
            self.reply(message, reply, parse_mode='HTML')
            return

        trackinfo = '<a href="{0}">{1}</a> - <a href="{2}">{3}</a>'.format(
            telegram_escape(current_track.get_artist().get_url()),
            telegram_escape(current_track.get_artist().get_name()),
            telegram_escape(current_track.get_url()),
            telegram_escape(current_track.get_title()))

        if current_track.get_userloved():
            trackinfo += ' [:heart:]️️'

        self.reply(message, '<a href="http://www.last.fm/user/{0}">{1}</a> is now listening to {2}'.format(
            telegram_escape(username), telegram_escape(user.first_name), trackinfo), parse_mode='HTML', emojify=True)
