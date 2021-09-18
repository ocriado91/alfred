#!/usr/bin/env python3

import alfred_bot
from TelegramBot.telegrambot import TelegramBot

alfred = alfred_bot.AlfredBot('test/config/alfred.toml')

def test_processingMessage():

    message = 'Check tasks'
    api_phrases = alfred.get_api_keyphrase()
    # Check if the message is in the list of API keyphrases
    assert message in api_phrases

def test_read_config():
    config = alfred.read_config()
    assert config['Miscellaneous']['TESTING']

def test_read_empty_config():
    alfred = alfred_bot.AlfredBot('test/config/alfred2.toml')
    config = alfred.read_config()
    assert config['Miscellaneous']['TESTING'] == True



