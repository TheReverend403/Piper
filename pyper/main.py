#!/usr/bin/env python3
import configparser
import logging
import sys

import os

from pyper.bot import Bot


def main(args):
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('googleapiclient.discovery').setLevel(logging.WARNING)
    if '--verbose' in args:
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(name)s: %(message)s')

    config = configparser.ConfigParser()
    config.read('config.ini')

    if not os.path.exists('data'):
        os.mkdir('data')

    bot = Bot(config)
    bot.poll()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
