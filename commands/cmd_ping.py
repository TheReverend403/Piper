import requests

from lib.command import Command


# https://github.com/amureki/isup/blob/master/isup/main.py
def get_status(host):
    website_url = '{0}{1}.json'.format('http://isitup.org/', host)
    response = requests.get(website_url)
    data = response.json()
    return data.get('status_code', 0), data.get('response_ip', 0), data.get('response_time', 0)


class PingCommand(Command):
    name = 'ping'
    aliases = ['isup']
    description = 'Checks whether a given host is up.'

    def run(self, message, args):
        if not args:
            self.reply(message, 'Please supply a host to check.')
            return

        host = args[0].strip()
        status, ip, response_time = get_status(host)
        if status == 1:
            response = '{0} ({1}) is up ({2} seconds).'.format(host, ip, response_time)
        elif status == 2:
            response = '{0} looks down from here!'.format(host)
        elif status == 3:
            response = '{0} doesn\'t appear to be a valid hostname!'.format(host)
        else:
            response = 'isitup.org api error'
        self.reply(message, response, disable_web_page_preview=True)
