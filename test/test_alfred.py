#!/usr/bin/env python3

import pytest
import alfredBot
from TelegramBot.telegrambot import TelegramBot
import sys

alfred = alfredBot.alfredBot('test/config/alfred.toml')

def test_alfred_get_api_list():
    assert list(alfred.get_API_list()) == ['GoogleTasks', 
                                           'GoogleCalendar', 
                                           'Github']

def test_processingMessage():
    message = 'Check tasks'
    aphi_phrases = alfred.get_API_keyphrase()

    # Check if the message is in the list of API keyphrases
    assert message in aphi_phrases

def test_read_config():
    config = alfred.read_config()
    assert config['Miscellaneous']['TESTING']



