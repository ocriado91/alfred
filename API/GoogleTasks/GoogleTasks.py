#!/usr/bin/env python3

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from API.API_abstract import API
from enum import Enum
# Define states
class States(Enum):
    INIT = 1
    TASK_LIST = 2

import logging
logger = logging.getLogger(__name__)

import sys

''' Google Task API to retrieve task list
    and tasks '''

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']


class GoogleTasks(API):
    ''' Google Tasks class '''

    def __init__(self,
                 config: dict):

        logger.info(f'Init Google Tasks!!!')

        self.state = States.INIT
        self.retry = 0

        logger.info('Starting Google Tasks')
        # Define attributes
        self.tasks_list = []
        self.tasks = []

        # Init credentials
        configpath = config['API']['GoogleTasks']['path']
        credentials_file = config['API']['GoogleTasks']['credentials']
        self.get_credentials(configpath)
        self.show_options()

    def show_options(self):
        message = 'Please select an option:\n'
        message += '1) Get task list\n'
        message += '2) Get tasks'
        return message

    def get_credentials(self,
                        configpath: str):
        '''Get Google Calendar credentials. The file token.pickle stores
         the user's access and refresh tokens, and is
         created automatically when the authorization flow completes for the first
         time. '''
        logger.info(f'Reading configuration file from {configpath}')
        creds = None
        token_path = os.path.join(configpath, 'token.pickle')
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print("Trying to open credentials.json file")
                credentials = os.path.join(configpath, 'client_secret.json')
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
        self.tasks_list = [x for x in items]

    def get_tasks_title(self):
        ''' Extract tasks title '''
        self.get_task_list()
        self.tasks_list_title = [x['title'] for x in self.tasks_list]
        return False

    def get_tasks(self,
                  task_item='My Tasks'):
        ''' This function search all tasks into
            specific task listitem '''

        self.get_task_list()
        for item in self.tasks_list:
            if item['title'] == task_item:
                taskID = item['id']
                tasks = self.service.tasks().list(tasklist=taskID).execute()
                for task_item in tasks['items']:
                    self.tasks.append(task_item['title'])

    def process_action(self, 
                       message: str,
                       retry: int):
        logger.info('Trying to process {message} at try = {self.retry}')
        if self.state == States.INIT:
            state_flag = self.get_tasks_title()
            if state_flag:
                logger.info("OK!!")
                self.state = States.INIT
            else:
                self.retry += 1
            logger.info(f'Retrying action number {self.retry}')
        


if __name__ == '__main__':

    configpath = sys.argv[1]
    tasks = GoogleTasks(configpath=configpath)

    # Show tasks list
    tasks.get_task_list()
    print('Getting tasklist')
    for task_item in tasks.tasks_list:
        print(task_item['title'])

    # Show tasks into Task Testing task list
    tasks.get_tasks(task_item='Task Testing')
    print('Getting tasks')
    for task_element in tasks.tasks:
        print(task_element)
