#!/usr/bin/env python3
import configparser
import logging
from sys import argv

from piper.bot import Bot


def main(args):
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('googleapiclient.discovery').setLevel(logging.WARNING)
    if '--verbose' in args:
        logging.basicConfig(level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read('config.ini')
    bot = Bot(config)
    bot.poll()


if __name__ == '__main__':
    main(argv)
