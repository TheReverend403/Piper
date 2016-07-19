from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from lib.command import Command
from lib.utils import escape_telegram_html


class GoogleCommand(Command):
    name = 'google'
    aliases = ['g', 'search']
    description = 'Searches Google for a set of search terms.'

    def run(self, message, args):
        if not self.config:
            self.reply(message, 'Google command is not configured!')
            self.logger.error('Google API keys are not configured.')
            return

        if not args:
            self.reply(message, 'Please supply some search terms!')
            return

        service = build('customsearch', 'v1', developerKey=self.config['api_key'])
        try:
            res = service.cse().list(q=' '.join(args), cx=self.config['custom_search_id'], num=5).execute()
        except HttpError as ex:
            self.reply(message, 'Error occurred while fetching search results!')
            self.logger.exception(ex)
            return

        if 'items' not in res:
            if 'error' in res:
                self.reply(message, res['error']['message'])
                return
            self.reply(message, 'No results found!')
            return

        results = res['items']
        search_information = res['searchInformation']
        reply = 'About {0} results ({1} seconds)\n'.format(search_information['formattedTotalResults'],
                                                           search_information['formattedSearchTime'])
        for idx, result in enumerate(results):
            title = result['title']
            url = result['formattedUrl']
            reply += '<b>{0}.</b> <a href="{2}">{1}</a>\n'.format(idx + 1, escape_telegram_html(title),
                                                                  escape_telegram_html(url))
        self.reply(message, reply, parse_mode='HTML')
