from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from lib.command import Command


class GoogleCommand(Command):
    name = 'google'
    aliases = ['g', 'search']
    description = 'Searches Google for a set of search terms.'

    def run(self, message, args):
        if not self.config:
            self.reply(message, 'Google command is not configured!')
            self.bot.logger.error('Google API keys are not configured.')
            return

        if len(args) == 0:
            self.reply(message, 'Please supply some search terms!')
            return

        service = build('customsearch', 'v1', developerKey=self.config['api_key'])
        try:
            res = service.cse().list(q=' '.join(args), cx=self.config['custom_search_id'], num=5).execute()
        except HttpError as ex:
            self.reply(message, 'Error occurred while fetching search results!')
            self.bot.logger.exception(ex)
            return

        if 'items' not in res:
            if 'error' in res:
                self.reply(message, res['error']['message'], disable_web_page_preview=True)
                return
            self.reply(message, 'No results found!', disable_web_page_preview=True)
            return

        results = res['items']
        search_information = res['searchInformation']
        reply = 'About {0} results ({1})\n'.format(search_information['formattedTotalResults'],
                                                   search_information['formattedSearchTime'])
        for idx, result in enumerate(results):
            title = result['title']
            url = result['formattedUrl']
            reply += '*{0}.* [{1}]({2} seconds)\n'.format(idx + 1, title, url)
        self.reply(message, reply, parse_mode='Markdown', disable_web_page_preview=True)
