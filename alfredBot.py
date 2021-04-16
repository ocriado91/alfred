#!/usr/bin/env python3

""" Alfred. A (Telegram Bot) Personal Assistant
"""

from TelegramBot.telegrambot import TelegramBot
from API.GoogleTasks.google_tasks import GoogleTasks
from API.Github.github_api import Github

import toml
import argparse
import logging
import sys

# Configure logging
LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
logging.basicConfig(format=LOG_FORMATTER)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PyGithub").setLevel(logging.WARNING)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class alfredBot():

    def __init__(self,
                 configfile: str):

        try:
            # Read Alfred Bot configuration
            self.configfile = configfile
            self.config = self.read_config()

            # Init Telegram Bot class
            telegram_config = self.config['TelegramBot']
            self.telegrambot = TelegramBot(telegram_config)

            # Init Google Task class
            configpath = self.config['API']['GoogleTasks']['path']
            self.googleTasks = GoogleTasks(configpath)

            # Init Github API wrapper class
            github_config = self.config['API']['Github']
            self.github = Github(github_config)

            last_message_id = -1
            while True:
                message_id = self.telegrambot.extract_message_id()
                # Discard first iteration until now incomingm message
                if last_message_id == -1:
                    last_message_id = message_id
                if message_id:
                    if message_id != last_message_id:
                        message = self.telegrambot.read_message()
                        self.processIncomingMessage(message)
                        last_message_id = message_id
                else:
                    break
        except KeyboardInterrupt:
            self.telegrambot.write_message('See you soon! :)')
            logger.info('Catched KeyboardInterrupt. Bye :)')
            sys.exit()

    def read_config(self):
        return toml.load(self.configfile)

    def getAPIList(self):
        return self.config['API'].keys()

    def processIncomingMessage(self,
                               message: str):
        logger.info(f'Received message: {message}')

        api_list = self.getAPIList()
        if message in api_list:
            logger.info(f'Detected {message} API')
        else:
            logger.warning(f'None API {message} detected')
            api_list_str = ','.join(api_list)
            logger.info(f'API list: {api_list_str}')
            self.telegrambot.write_message(f'Please insert a valid option {api_list_str}')


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
