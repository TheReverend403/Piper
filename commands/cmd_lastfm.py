import pylast

from lib.command import Command
from lib.utils import telegram_escape, emojify

SET_STRINGS = [
    '-s', '-set', '--set', 'set'
]

DB_KEY = 'lastfm_username'


class LastFMCommand(Command):
    name = 'lastfm'
    aliases = ['np', 'nowplaying']
    description = 'Post your currently playing song.'

    def __init__(self, bot, config):
        super().__init__(bot, config)
        try:
            self.__network = pylast.LastFMNetwork(api_key=self._config['api_key'])
        except pylast.NetworkError as ex:
            self._logger.exception(ex)
            self._config = None
        except KeyError:
            self._logger.error('last.fm API key is not configured.')
        except TypeError:
            self._logger.error('last.fm API key is not configured.')

    def run(self, message, args):
        if not self._config:
            self.reply(message, 'last.fm command is not configured!')
            return

        user = message.from_user
        if args and args[0] in SET_STRINGS:
            try:
                username = args[1].strip()
            except IndexError:
                self.reply(message, 'Please provide a username. (/np -s <username>)')
                return

            try:
                self.bot.database.set_user_value(user, DB_KEY,
                                                 self.__network.get_user(username).get_name(properly_capitalized=True))
                self.reply(message, 'last.fm username set.')
            except pylast.WSError:
                self.reply(message, 'No such last.fm user. Are you trying to trick me? :^)')
            return

        username = self.bot.database.get_user_value(user, DB_KEY)
        if not username:
            self.reply(message, 'You have no last.fm username set. Please set one with /np -s <username>')
            return

        self.bot.telegram.send_chat_action(message.chat.id, 'typing')
        lastfm_user = self.__network.get_user(username)
        current_track = lastfm_user.get_now_playing()
        if not current_track:
            reply = '<a href="http://www.last.fm/user/{0}">{1}</a> is not listening to anything right now.'.format(
                telegram_escape(username),
                telegram_escape(user.first_name))
            self.reply(message, reply, parse_mode='HTML')
            return

        trackinfo = '<a href="{0}">{1}</a> - <a href="{2}">{3}</a>'.format(
            telegram_escape(current_track.get_artist().get_url()),
            telegram_escape(current_track.get_artist().get_name()),
            telegram_escape(current_track.get_url()),
            telegram_escape(current_track.get_title()))

        try:
            if current_track.get_userloved():
                trackinfo += emojify(' [:heart:]️️')
        except pylast.WSError:
            pass

        reply = '<a href="http://www.last.fm/user/{0}">{1}</a> is now listening to {2}'.format(
            telegram_escape(username), telegram_escape(user.first_name), trackinfo)

        currently_listening = current_track.get_listener_count() - 1
        if currently_listening:
            reply += ', and so {0} {1} other {2}.'.format(
                'is' if currently_listening is 1 else 'are', currently_listening,
                'user' if currently_listening is 1 else 'users')
        else:
            reply += ', and is the only user currently doing so.'

        self.reply(message, reply, parse_mode='HTML')
