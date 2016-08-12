from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from lib.command import Command
from lib.utils import telegram_escape


class GoogleCommand(Command):
    name = 'google'
    aliases = ['g', 'search']
    description = 'Searches Google for a set of search terms.'

    def __init__(self, bot, config):
        super().__init__(bot, config)
        try:
            self.__service = build('customsearch', 'v1', developerKey=self._config['api_key'])
        except (KeyError, HttpError, TypeError) as ex:
            self._logger.exception(ex)
            self._config = None

    def run(self, message, args):
        if not self._config:
            self.reply(message, 'Google command is not configured!')
            return

        if not args:
            self.reply(message, 'Please supply some search terms!')
            return

        try:
            self.bot.telegram.send_chat_action(message.chat.id, 'typing')
            res = self.__service.cse().list(q=' '.join(args), cx=self._config['custom_search_id'], num=5).execute()
        except HttpError as ex:
            self.reply(message, 'Error occurred while fetching search results!')
            self._logger.exception(ex)
            return

        try:
            results = res['items']
            search_information = res['searchInformation']
            reply = 'About {0} results ({1} seconds)\n'.format(search_information['formattedTotalResults'],
                                                               search_information['formattedSearchTime'])
            for idx, result in enumerate(results):
                title = result['title']
                url = result['link']
                display_url = result['displayLink']
                reply += '<b>{0}.</b> <a href="{1}">{2}</a>\n<code>{3}</code>\n'.format(idx + 1, telegram_escape(url),
                                                                                        telegram_escape(title),
                                                                                        telegram_escape(display_url))
        except KeyError:
            try:
                self.reply(message, res['error']['message'])
            except KeyError:
                self.reply(message, 'No results found')
            finally:
                return

        self.reply(message, reply, parse_mode='HTML')
