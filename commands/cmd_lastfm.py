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
    description = 'Post your currently playing song.'
    has_database = True

    def run(self, message, args):
        if not self.config:
            self.reply(message, 'last.fm command is not configured!')
            self.logger.error('last.fm API key is not configured.')
            return

        if not message.from_user.username:
            self.reply(message, 'You do not have a Telegram username I can use with last.fm!')
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
                self.database.set_user_value(user, 'username', username)
                self.reply(message, 'last.fm username set.')
            else:
                self.reply(message, 'No such last.fm user. Are you trying to trick me? :^)')
            return

        username = self.database.get_user_value(user, 'username')
        if not username:
            self.reply(message, 'You have no last.fm username set. Please set one with /np -s <username>')
            return

        user = network.get_user(username)
        if not user:
            self.reply(message, '{0} doesn\'t appear to have a last.fm account!'.format(username))
            return

        current_track = user.get_now_playing()
        if not current_track:
            reply = '<a href="http://www.last.fm/user/{0}">{0}</a> is not listening to anything right now.'.format(
                escape_telegram_html(username))
            self.reply(message, reply, parse_mode='HTML')
            return

        trackinfo = '<a href="{0}">{1} - {2}</a>'.format(
            escape_telegram_html(current_track.get_url()),
            escape_telegram_html(current_track.get_artist().get_name()),
            escape_telegram_html(current_track.get_title()))

        self.reply(message, '<a href="http://www.last.fm/user/{0}">{0}</a> is now listening to {1}.'.format(
            escape_telegram_html(username), trackinfo), parse_mode='HTML')
