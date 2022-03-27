#!/usr/bin/env python3
''' Google Tasks Python API '''

import logging
import sys

import tomli
from API.api_abstract import API
from API.Google.google_common import GoogleCommon

logger = logging.getLogger(__name__)


''' Google Task API to retrieve task list
    and tasks '''

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']


class GoogleTasks(API, GoogleCommon):
    ''' Google Tasks class '''

    def __init__(self,
                 configpath: str):

        logger.info('Starting Google Tasks')

        # Define attributes
        self.list = []
        self.items = []
        self.tasks = []

        # Init credentials
        with open(configpath, 'rb') as config_file:
            config = tomli.load(config_file)
        configfile = config['API']['Google']['Common']['path']
        self.get_credentials(configfile,
                             scopes=['https://www.googleapis.com/auth/tasks.readonly'])

    def get_list(self):
        ''' Read tasklist and save it into attribute '''
        results = self.service.tasklists().list(maxResults=10).execute()
        self.items = results.get('items', [])
        self.list = [x['title'] for x in self.items]

    def get_tasks(self,
                  target_tasklist='My Tasks'):
        '''  Read all tasks specific task list '''

        self.get_list()
        for item in self.items:
            if item['title'] == target_tasklist:
                task_id = item['id']
                tasks_ = self.service.tasks().list(tasklist=task_id).execute()
                # Try to extract all tasks from list or set to empty list
                # if no tasks are found
                try:
                    for element in tasks_['items']:
                        self.tasks.append(element['title'])
                except KeyError:
                    self.tasks = None

    def process_action(self, message: str):
        ''' Process Google Tasks action'''
        if message == 'Check tasks':
            logger.debug('Detected API message %s', message)
            self.get_tasks()
            return ','.join(self.tasks)
        elif message == 'Check list':
            logger.debug('Detected API message %s', message)
            self.get_list()
            return '\n'.join(self.list)
        logger.debug('Successfully processed Google Tasks action')
        return None


if __name__ == '__main__':

    configpath = sys.argv[1]
    logger.debug(f'Reading {configpath}')
    tasks = GoogleTasks(configpath)

    # Show tasks list
    tasks.get_tasklist()
    print('Getting tasklist')
    for task_item in tasks.tasks_list:
        print(task_item['title'])

    # Show tasks into Task Testing task list
    tasks.get_tasks(target_tasklist='Task Testing')
    print('Getting tasks')
    for task_element in tasks.tasks:
        print(task_element)
