#!/usr/bin/env python3

''' Telegram Bot API based on official Telegram Bot API requests
    Reference: https://core.telegram.org/bots/api s'''


import logging
import sys
import requests

logger = logging.getLogger(__name__)


class TelegramBot():
    ''' Telegram Bot Class '''

    def __init__(self,
                 config: dict):
        self.config = config
        self.chat_id = None
        logger.info("Initialised Telegrambot")

    def extract_message_id(self):
        ''' Extract the message ID required to establish
            channel chat between AlfredBot and Bruce Wayne :) '''

        url = f'''https://api.telegram.org/bot{self.config['API_KEY']}/getUpdates'''
        data = requests.post(url).json()

        # Extract the chat ID field from the newest incoming message
        if data['result']:
            self.chat_id = data['result'][-1]['message']['chat']['id']
            return data['result'][-1]['update_id']
        logger.warning('No detected messages.\
            Plese send a message to Alfred to establish communication')
        return None

    def read_message(self):
        ''' Read message from official TelegramBot API request '''

        url = f'''https://api.telegram.org/bot{self.config['API_KEY']}/getUpdates'''
        data = requests.post(url).json()

        # Extract text from last incoming data
        message = data['result'][-1]['message']['text']
        return message

    def send_message(self,
                      message: str):
        ''' Sent message from official TelegramBot API request '''

        url = f'''https://api.telegram.org/bot{self.config['API_KEY']}/sendMessage'''
        data = {'chat_id': self.chat_id, 'text': message}
        requests.post(url, data).json()


def main():
    ''' Main function '''

    # Read configfile
    config = sys.argv[1]

    # Echo received text
    telegrambot = TelegramBot(config)
    mesage = telegrambot.read_message()
    telegrambot.send_message(mesage)


if __name__ == '__main__':
    main()
