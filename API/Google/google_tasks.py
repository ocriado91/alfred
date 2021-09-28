#!/usr/bin/env python3
''' Google Tasks Python API '''

import logging
import os.path
import pickle
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from API.api_abstract import API
logger = logging.getLogger(__name__)


''' Google Task API to retrieve task list
    and tasks '''

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']


class GoogleTasks(API):
    ''' Google Tasks class '''

    def __init__(self,
                 config: dict):

        logger.info('Starting Google Tasks')
        # Define attributes
        self.tasks_list_title = []
        self.tasks_list = []
        self.tasks = []

        # Init credentials
        configfile = config['API']['Google']['Common']['path']
        self.get_credentials(configfile)

    def get_credentials(self,
                        configfile: str):
        '''Get Google Calendar credentials. The file token.pickle stores
         the user's access and refresh tokens, and is
         created automatically when the authorization flow completes for the first
         time. '''
        logger.info('Reading configuration file from %s', configfile)
        creds = None
        token_path = os.path.join(configfile, 'token.pickle')
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print("Trying to open credentials.json file")
                credentials = os.path.join(configfile, 'client_secret.json')
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('tasks', 'v1', credentials=creds)

    def get_task_list(self):
        ''' Retrieve task list '''
        results = self.service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])
        self.tasks_list = list(items)

    def check_tasks(self):
        ''' Extract tasks title as string'''
        self.get_task_list()
        self.tasks_list_title = [x['title'] for x in self.tasks_list]
        self.tasks_list = ','.join(self.tasks_list_title)

    def get_tasks(self,
                  check_item='My Tasks'):
        ''' This function search all tasks into
            specific task listitem '''

        self.get_task_list()
        for item in self.tasks_list:
            if item['title'] == check_item:
                task_id = item['id']
                tasks_ = self.service.tasks().list(tasklist=task_id).execute()
                for element in tasks_['items']:
                    self.tasks.append(element['title'])

    def process_action(self, message: str):
        ''' Process Google Tasks action'''
        if message == 'Check tasks':
            logger.debug('Detected API message %s', message)
            self.check_tasks()
            return self.tasks_list
        elif message == 'Check task list':
            logger.debug('Detected API message %s', message)
            self.check
        return None


if __name__ == '__main__':

    configpath = sys.argv[1]
    tasks = GoogleTasks(configpath)

    # Show tasks list
    tasks.get_task_list()
    print('Getting tasklist')
    for task_item in tasks.tasks_list:
        print(task_item['title'])

    # Show tasks into Task Testing task list
    tasks.get_tasks(check_item='Task Testing')
    print('Getting tasks')
    for task_element in tasks.tasks:
        print(task_element)
