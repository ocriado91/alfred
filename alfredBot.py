#!/usr/bin/env python3

""" Alfred. A (Telegram Bot) Personal Assistant
"""

from API.GoogleTasks.google_tasks import GoogleTasks
from TelegramBot.telegrambot import TelegramBot
import toml
import os
import argparse


class alfredBot():

    def __init__(self,
                 configfile: str):

        # Read Alfred Bot configuration
        self.configfile = configfile
        config = self.read_config()
        
        # Init Google Task class
        configpath = config['API']['Google']['Tasks']['path'] 
        self.googleTasks = GoogleTasks(configpath)

        telegram_config = config['API']['TelegramBot']
        self.telegrambot = TelegramBot(telegram_config)

        last_message_id = -1
        while True:
            message_id = self.telegrambot.extract_message_id()
            if message_id != last_message_id:
                self.telegrambot.read_message()
                last_message_id = message_id
                self.telegrambot.write_message("Received message!")

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