#!/usr/bin/env python3

import pytest
import alfredBot
from TelegramBot.telegrambot import TelegramBot
import sys

alfred = alfredBot.alfredBot('test/config/alfred.toml')

def test_processingMessage():
    message = 'Check tasks'
    api_phrases = alfred.get_API_keyphrase()
    print(api_phrases)
    # Check if the message is in the list of API keyphrases
    assert message in api_phrases

def test_read_config():
    config = alfred.read_config('test/config/alfred.toml')
    assert config['Miscellaneous']['TESTING']

def test_read_empty_config():
    config = alfred.read_config('test/config/alfred2.toml')
    assert config['Miscellaneous']['TESTING'] == False



