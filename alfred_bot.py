#!/usr/bin/env python3

""" Alfred. A (Telegram Bot) Personal Assistant
"""

import argparse
import importlib
import logging
import sys
import toml

from TelegramBot.telegrambot import TelegramBot


# Configure logging
LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
logging.basicConfig(format=LOG_FORMATTER)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PyGithub").setLevel(logging.WARNING)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class AlfredBot():
    ''' Alfred Bot main class '''

    def __init__(self,
                 configfile: str):

        try:
            logger.debug('Starting AlfredBot')
            # Read Alfred Bot configuration file
            self.configfile = configfile
            self.config = self.read_config()

            # Init Telegram Bot class
            telegram_config = self.config['TelegramBot']
            self.telegrambot = TelegramBot(telegram_config)

            # Only execute Telegram Bot polling if testing
            # is not enabled into configile
            if not self.config['Miscellaneous']['TESTING']:
                self.telegram_polling()

        except KeyboardInterrupt:
            self.telegrambot.write_message('See you soon! :)')
            logger.info('Catched KeyboardInterrupt. Bye :)')
            sys.exit()

    def read_config(self):
        ''' Read Alfred TOML configuration file '''

        config = toml.load(self.configfile)
        # Disable testing if Miscellaneus section
        # is not defined as key into configuration dictionary
        if 'Miscellaneous' not in config.keys():
            config['Miscellaneous'] = {'TESTING': True}
        return config

    def telegram_polling(self):
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
                    self.processing_incoming_message(message)
                    last_message_id = message_id
            else:
                break

    def get_api_keyphrase(self):
        ''' Get list of API keyphrases '''

        phrases = []
        # Extract API packages defined into configuration file
        packages = self.config['API'].keys()
        logger.debug('API packages %s', packages)
        for package in packages:

            # Extract API modules from each API package
            modules = self.config['API'][package].keys()
            logger.debug('API modules %s', modules)
            for module in modules:

                # Extract API actions from each API modules
                actions = self.config['API'][package][module].keys()
                logger.debug('Actions %s', actions)
                for action in actions:
                    # Try to extract phrase from API action configuration
                    try:
                        phrases.append(self.config['API'][package][module][action]['phrase'])
                    # Except KeyError if no phrase is defined and TypeError if no action is defined
                    except (KeyError, TypeError):
                        continue
        return phrases

    def get_api_function(self, phrase: str):
        ''' Get API and function through phrase'''

        packages = self.config['API'].keys()
        logger.debug('API packages %s', packages)
        for package in packages:
            modules = self.config['API'][package].keys()
            for module in modules:
                actions = self.config['API'][package][module].keys()
                for action in actions:
                    try:
                        if phrase == self.config['API'][package][module][action]['phrase']:
                            return f'API.{package}.{module}'
                    except (KeyError, TypeError):
                        continue
        return None

    def processing_incoming_message(self,
                                    message: str):

        ''' Check incoming message and compare against
            phrases defined by configuration'''

        logger.info('Received message: %s', message)
        api_phrases = self.get_api_keyphrase()
        # Log list of API keyphrases
        logger.debug('API keyphrase %s', api_phrases)
        if message in api_phrases:

            # Get API and function through message
            module_name = self.get_api_function(message)
            logger.debug('Module name %s', module_name)
            module = importlib.import_module(module_name)
            class_name = module_name.split('.')[-1]
            dynamic_class = getattr(module, class_name)
            result = dynamic_class(self.config).process_action(message)
            logger.debug('Result: %s', result)
            self.telegrambot.write_message(result)
        else:
            logger.info('No API phrase found for %s', message)
            self.telegrambot.write_message(f"I don't have any action for {message}.\
                                             Please, try again")


def argument_parser():
    ''' Argument parser '''

    args = argparse.ArgumentParser()
    args.add_argument('--config',
                      help='''AlfredBot's main configfile''',
                      default='config/alfred.toml')

    return args.parse_args()


def main():
    ''' Main function '''

    # Argument parser
    args = argument_parser()

    # Launch AlfredBot
    AlfredBot(args.config)


if __name__ == '__main__':
    main()
