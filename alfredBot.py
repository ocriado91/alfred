#!/usr/bin/env python3

""" Alfred. A (Telegram Bot) Personal Assistant
"""

from API.GoogleTasks.google_tasks import GoogleTasks
import toml
import os


class alfredBot():

    def __init__(self):

        # Read Alfred Bot configuration
        config = self.read_config()
        
        # Init Google Task class
        configpath = config['API']['Google']['Tasks']['path'] 
        self.googleTasks = GoogleTasks(configpath)

    def read_config(self):
        return toml.load('config/alfred.toml')

def main():

    alfredBot()
    


if __name__ == '__main__':
    main()