import pylast
from lib.command import Command
from lib.utils import escape_telegram_html

ADD_STRINGS = [
    "-a", "-add", "--add",
    "-s", "-set", "--set"
]


class LastFMCommand(Command):
    name = 'lastfm'
    aliases = ['np', 'nowplaying']
    description = 'Post your currently playing song (Telegram username must be the same as last.fm username).'

    def run(self, message, args):
        if not self.config:
            self.reply(message, 'last.fm command is not configured!', disable_web_page_preview=True)
            self.logger.error('last.fm API key is not configured.')
            return

        if not message.from_user.username:
            self.reply(message, 'You do not have a Telegram username I can use with last.fm!',
                       disable_web_page_preview=True)
            return

        network = pylast.LastFMNetwork(api_key=self.config['api_key'])

        user = message.from_user
        if args and args[0] in ADD_STRINGS:
            if len(args) == 1:
                self.reply(message, 'Please provide a username. (/np -s <username>)')
                return
            username = args[1].strip()
            user_exists = False
            try:
                network.get_user(username).get_id()
                user_exists = True
            except pylast.WSError:
                pass
            if user_exists:
                self.bot.database.set_user_value(user, 'lastfm_username', username)
                self.reply(message, 'last.fm username set.', disable_web_page_preview=True)
            else:
                self.reply(message, 'No such last.fm user. Are you trying to trick me? :^)',
                           disable_web_page_preview=True)
            return

        username = self.bot.database.get_user_value(user, 'lastfm_username')
        if not username:
            self.reply(message, 'You have no last.fm username set. Please set one with /np -s <username>',
                       disable_web_page_preview=True)
            return

        user = network.get_user(username)
        if not user:
            self.reply(message, '{0} doesn\'t appear to have a last.fm account!'.format(username),
                       disable_web_page_preview=True)
            return

        current_track = user.get_now_playing()
        if not current_track:
            self.reply(message, '{0} is not listening to anything right now.'.format(username))
            return

        trackinfo = '<a href="{0}">{1} - {2}</a>'.format(
            escape_telegram_html(current_track.get_url()),
            escape_telegram_html(current_track.get_artist().get_name()),
            escape_telegram_html(current_track.get_title()))

        self.reply(message, '{0} is now listening to {1}'.format(username, trackinfo),
                   parse_mode='HTML', disable_web_page_preview=True)
