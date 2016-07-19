import pylast
from lib.command import Command
from lib.utils import escape_telegram_html


class LastFMCommand(Command):
    name = 'lastfm'
    aliases = ['np', 'nowplaying']
    description = 'Post your currently playing song (Telegram username must be the same as last.fm username).'

    def run(self, message, args):
        if not self.config:
            self.reply(message, 'last.fm command is not configured!')
            self.logger.error('last.fm API key is not configured.')
            return

        if not message.from_user.username:
            self.reply(message, 'You do not have a Telegram username I can use with last.fm!')
            return

        network = pylast.LastFMNetwork(api_key=self.config['api_key'])
        username = message.from_user.username
        user = network.get_user(username)
        if not user:
            self.reply(message, '{0} doesn\'t appear to have a last.fm account!'.format(username))
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
