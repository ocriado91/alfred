#!/usr/bin/env python3

""" Alfred. A (Telegram Bot) Personal Assistant
"""

from TelegramBot.telegrambot import TelegramBot

import toml
import argparse
import logging
import sys
import importlib

# Configure logging
LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
logging.basicConfig(format=LOG_FORMATTER)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PyGithub").setLevel(logging.WARNING)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class alfredBot():

    def __init__(self,
                 configfile: str):

        try:
            logger.debug('Starting AlfredBot')
            # Read Alfred Bot configuration
            self.configfile = configfile
            self.config = self.read_config()

            # Init Telegram Bot class
            telegram_config = self.config['TelegramBot']
            self.telegrambot = TelegramBot(telegram_config)

            # Only execute Telegram Bot polling if testing 
            # is not enabled into configile
            if not self.config['Miscellaneous']['TESTING']:
                self.telegramPolling()

        except KeyboardInterrupt:
            self.telegrambot.write_message('See you soon! :)')
            logger.info('Catched KeyboardInterrupt. Bye :)')
            sys.exit()

    def telegramPolling(self):
        ''' Read new Telegram messages through
            pollin mechanism'''
        last_message_id = -1
        while True:
            message_id = self.telegrambot.extract_message_id()
            # Discard first iteration until now incoming message
            if last_message_id == -1:
                last_message_id = message_id
            if message_id:
                if message_id != last_message_id:
                    message = self.telegrambot.read_message()
                    self.processIncomingMessage(message)
                    last_message_id = message_id
            else:
                break


    def read_config(self):
        config = toml.load(self.configfile)
        # Disable testing if not enabled in configuration file
        if not config['Miscellaneous']['TESTING']:
            logger.info('Testing is disabled')
            config['Miscellaneous']['TESTING'] = False
        return config

    def get_API_list(self):
        return self.config['API'].keys()

    def get_API_keyphrase(self):

        phrases = []
        # Extract API types defined into configuration file
        types = self.config['API'].keys()
        for type in types:

            # Extract API actions from each API type
            actions = self.config['API'][type].keys()
            for action in actions:
                # Try to extract phrase from API action configuration
                try:
                    phrases.append(self.config['API'][type][action]['phrase'])
                except KeyError:
                    logger.debug(f'No phrase found for action {action}')
                    continue

        return phrases

    def processIncomingMessage(self,
                               message: str):
        logger.info(f'Received message: {message}')
        api_phrases = self.get_API_keyphrase()
        if message in api_phrases:
            logger.info(f'Found API phrase {message}')
            self.telegrambot.write_message(f'Found API phrase {message}')
        else:
            logger.info(f'No API phrase found for {message}')
            self.telegrambot.write_message(f'No API phrase found for {message}')


def argument_parser():

    args = argparse.ArgumentParser()
    args.add_argument('--config',
                      help='''AlfredBot's main configfile''',
                      default='config/alfred.toml')

    return args.parse_args()


def main():

    # Argument parser
    args = argument_parser()

    # Launch AlfredBot
    alfredBot(args.config)


if __name__ == '__main__':
    main()
