#!/usr/bin/env python3
''' Alfred Bot Unit Testing '''

import alfred_bot

alfred = alfred_bot.AlfredBot('test/config/alfred.toml')


def test_processing_message():
    ''' Testing Google Tasks API Check tasks phrase'''
    message = 'Check tasks'
    api_phrases = alfred.get_api_keyphrase()
    # Check if the message is in the list of API keyphrases
    assert message in api_phrases


def test_read_config():
    ''' Testing value into miscellanueous section
        of configuration file
    '''
    config = alfred.read_config()
    assert config['Miscellaneous']['TESTING']


def test_read_empty_config():
    ''' Testing value into miscellaneuous section
        in case of empty field
    '''
    alfred2 = alfred_bot.AlfredBot('test/config/alfred2.toml')
    config = alfred2.read_config()
    assert config['Miscellaneous']['TESTING']
