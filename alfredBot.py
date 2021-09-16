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
            # Read Alfred Bot configuration file
            self.config = self.read_config(configfile)

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


    def read_config(self,
                    configfile: str = None):
        config = toml.load(configfile)
        # Disable testing if Miscellaneus section 
        # is not defined as key into configuration dictionary
        if 'Miscellaneous' not in config.keys():
            config['Miscellaneous'] = {'TESTING': False}
        return config

    def get_API_keyphrase(self):

        phrases = []
        # Extract API packages defined into configuration file
        packages = self.config['API'].keys()
        logger.debug(f'API packages: {packages}')
        for package in packages:

            # Extract API modules from each API package
            modules = self.config['API'][package].keys()
            logger.debug(f'API modules: {modules}')
            for module in modules:

                # Extract API actions from each API modules
                actions = self.config['API'][package][module].keys()
                logger.debug(f'Actions: {actions}')
                for action in actions:
                    # Try to extract phrase from API action configuration
                    try:
                        phrases.append(self.config['API'][package][module][action]['phrase'])
                    # Except KeyError if no phrase is defined and TypeError if no action is defined
                    except (KeyError, TypeError):
                        continue
        return phrases

    def getAPIFunction(self, phrase: str):
        ''' Get API and function through phrase'''

        packages = self.config['API'].keys()
        logger.debug(f'API packages: {packages}')
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

    def processIncomingMessage(self,
                               message: str):

        ''' Check incoming message and compare against
            phrases defined by configuration'''

        logger.info(f'Received message: {message}')
        api_phrases = self.get_API_keyphrase()
        # Log list of API keyphrases
        logger.debug(f'API keyphrases: {api_phrases}')
        if message in api_phrases:

            # Get API and function through message
            module_name = self.getAPIFunction(message)
            logger.debug(f'Module name: {module_name}')
            module = importlib.import_module(module_name)
            class_name = module_name.split('.')[-1]
            dynamic_class = getattr(module, class_name)
            result = dynamic_class(self.config).process_action(message)
            logger.debug(f'Result: {result}')
            self.telegrambot.write_message(result)
        else:
            logger.info(f'No API phrase found for {message}')
            self.telegrambot.write_message(f"I don't have any action for {message}. Please, try again")


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
