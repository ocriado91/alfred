#!/usr/bin/env python3

""" Alfred. A (Telegram Bot) Personal Assistant
"""

from TelegramBot.telegrambot import TelegramBot
from API.GoogleTasks.google_tasks import GoogleTasks
from API.Github.github_api import Github

import toml
import os
import argparse
import logging

# Configure logging
LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
logging.basicConfig(format=LOG_FORMATTER)
logging.getLogger("urllib3").setLevel(logging.WARNING) # Disable urllib3 debug log messages
logging.getLogger("PyGithub").setLevel(logging.WARNING)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class alfredBot():

    def __init__(self,
                 configfile: str):

        # Read Alfred Bot configuration
        self.configfile = configfile
        config = self.read_config()

        # Init Telegram Bot class
        telegram_config = config['TelegramBot']
        self.telegrambot = TelegramBot(telegram_config)
        
        # Init Google Task class
        configpath = config['API']['GoogleTasks']['path'] 
        self.googleTasks = GoogleTasks(configpath)

        # Init Github API wrapper class
        github_config = config['API']['Github']
        self.github = Github(github_config)

        last_message_id = -1
        while True:
            message_id = self.telegrambot.extract_message_id()
            if message_id:
                if message_id != last_message_id:
                    logger.info("Received new message")
                    self.telegrambot.read_message()
                    last_message_id = message_id
                    self.telegrambot.write_message("Received message!")
            else:
                break

    def read_config(self):
        return toml.load(self.configfile)

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