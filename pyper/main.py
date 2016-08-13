#!/usr/bin/env python3
import argparse
import configparser
import logging
import sys

import os

from pyper.bot import Bot


def main():
    parser = argparse.ArgumentParser(description='Pyper - A Python Telegram bot.')
    parser.add_argument('--loglevel', '-l', type=str, default='INFO',
                        help='Set the log level to INFO, WARNING, ERROR or DEBUG')
    args = parser.parse_args()

    logging.basicConfig(level=logging.getLevelName(args.loglevel), format='[%(levelname)-7s] %(name)s: %(message)s')
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('googleapiclient.discovery').setLevel(logging.WARNING)
    logging.getLogger('cachecontrol.controller').setLevel(logging.WARNING)

    config = configparser.ConfigParser()
    config.read('config.ini')

    if not os.path.exists('data'):
        os.mkdir('data')

    bot = Bot(config)
    bot.poll()


if __name__ == '__main__':
    sys.exit(main())
