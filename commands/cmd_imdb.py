from imdbpie import Imdb
from lib.command import Command
from lib.utils import escape_telegram_html


class ImdbCommand(Command):
    name = 'imdb'
    aliases = ['movie']
    description = 'Searches IMDB for movie titles.'

    def run(self, message, args):
        if not args:
            self.reply(message, 'Please supply some search terms.')
            return

        imdb = Imdb(cache=True, exclude_episodes=True)
        self.bot.telegram.send_chat_action(message.chat.id, 'typing')
        results = imdb.search_for_title(' '.join(args))
        if not results:
            self.reply(message, 'No results found!')
            return

        result = imdb.get_title_by_id(results[0]['imdb_id'])
        reply = '<b>URL:</b> http://www.imdb.com/title/{0}\n'.format(escape_telegram_html(result.imdb_id))
        reply += '<b>Title:</b> {0}\n'.format(escape_telegram_html(result.title))
        reply += '<b>Year:</b> {0}\n'.format(result.year)
        reply += '<b>Genre:</b> {0}\n'.format(escape_telegram_html(', '.join(result.genres[:3])))
        reply += '<b>Rating:</b> {0}\n'.format(result.rating)
        runtime, _ = divmod(result.runtime, 60)
        reply += '<b>Runtime:</b> {0} minutes\n'.format(runtime)
        reply += '<b>Certification:</b> {0}\n'.format(result.certification)
        reply += '<b>Cast:</b> {0}\n'.format(
            escape_telegram_html(', '.join([person.name for person in result.cast_summary[:5]])))
        reply += '<b>Director(s):</b> {0}\n\n'.format(
            escape_telegram_html(', '.join([person.name for person in result.directors_summary[:5]])))
        reply += escape_telegram_html(result.plots[0])

        self.reply(message, reply, parse_mode='HTML', disable_web_page_preview=True)
