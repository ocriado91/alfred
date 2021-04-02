#!/usr/bin/env python3

import requests
import sys
import toml

class TelegramBot():

    def __init__(self,
                 config: dict):
        self.config = config


    def extract_message_id(self):
        url = f'''https://api.telegram.org/bot{self.config['API_KEY']}/getUpdates'''
        data = requests.post(url).json()
        # Extract the chat ID field from the newest incoming message
        self.chat_id = data['result'][-1]['message']['chat']['id']
        return data['result'][-1]['update_id']

    def read_message(self):

        url = f'''https://api.telegram.org/bot{self.config['API_KEY']}/getUpdates'''
        data = requests.post(url).json()
        return data['result'][-1]['message']['text']

    def write_message(self,
                      message: str):

        url = f'''https://api.telegram.org/bot{self.config['API_KEY']}/sendMessage'''
        data = {'chat_id': self.chat_id, 'text': message}
        requests.post(url, data).json()




def main():

    # Read configfile
    config = sys.argv[1]

    # Echo received text
    telegrambot = TelegramBot(config)
    text = telegrambot.read_message()
    telegrambot.write_message(text)

if __name__ == '__main__':
    main()