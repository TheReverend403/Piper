import datetime
import ujson as json

import dateutil.relativedelta
import requests

from lib.command import Command
from lib.utils import telegram_escape, emojify


class RedditCommand(Command):
    name = 'reddit'
    aliases = ['r']
    description = 'Gets account info for a given reddit username.'

    def run(self, message, args):
        if not args:
            self.reply(message, 'Please supply a username!')
            return

        response = None
        try:
            headers = {'User-Agent': 'Pyper, by /u/TheReverend403 - https://github.com/TheReverend403/Pyper'}
            profile_url = 'http://www.reddit.com/user/{0}/about.json'.format(args[0])
            self.bot.telegram.send_chat_action(message.chat.id, 'typing')
            response = requests.get(profile_url, headers=headers)
        except requests.exceptions.RequestException as ex:
            self.reply(message, 'Error: {0}'.format(ex.strerror))
            self._logger.exception(ex)
            return
        finally:
            if response is not None:
                response.close()

        response_data = json.loads(response.text)
        try:
            user_data = response_data['data']
            canonical_username = user_data['name']
            pretty_username = '/u/{0}'.format(canonical_username)
            link_karma = user_data['link_karma']
            comment_karma = user_data['comment_karma']
            is_gold = user_data['is_gold']
            is_verified = user_data['has_verified_email']

            joined = datetime.datetime.fromtimestamp(user_data['created_utc'])
            diff = dateutil.relativedelta.relativedelta(joined, datetime.datetime.now())
            joined_time = joined.strftime('%B %d, %Y')
            joined_string = '{0} ({1} years, {2} months ago)'.format(joined_time, abs(diff.years), abs(diff.months))
        except KeyError:
            try:
                self.reply(message, 'Error: {0}'.format(response_data['message']))
            except KeyError as ex:
                self.reply(message, str(ex))
            return

        reply = '<b>Account info for</b> <a href="https://reddit.com{0}">{0}</a>'.format(
            telegram_escape(pretty_username))
        if is_gold or is_verified:
            reply += ' ('
            if is_gold:
                reply += emojify(':trophy:')
            if is_verified:
                reply += emojify(':envelope:')
            reply += ')'
        reply += '\n'
        reply += '<b>Link Karma:</b> {0}\n'.format(link_karma)
        reply += '<b>Comment Karma:</b> {0}\n'.format(comment_karma)
        reply += '<b>Total Karma:</b> {0}\n'.format(comment_karma + link_karma)
        reply += '<b>Registered:</b> {0}\n'.format(joined_string)
        self.reply(message, reply, parse_mode='HTML')
