#!/usr/bin/env python3

''' Github Class wrapper through PyGithub'''

import logging
import sys
import github
import tomli
from API.api_abstract import API

logger = logging.getLogger(__name__)


class Github(API):
    ''' Wrapper Github class of PyGithub '''
    def __init__(self,
                 config: dict):

        logger.info('Starting Github API')
        github_api_key = config['Common']['API_KEY']
        self.github = github.Github(github_api_key)
        self.commit_date = None

    def get_last_commit_date(self):
        ''' Extract date of last commit '''
        commits = []
        repos = self.github.get_user().get_repos()
        for repo in repos:
            branch = repo.get_branch('main')
            commit = branch.commit
            commits.append(commit)

        # Extract last commit
        self.commit_date = commits[-1].commit.author.date

    def process_action(self,
                       message: str):
        ''' Process action '''
        pass


def main():
    ''' Main function '''

    configpath = sys.argv[1]
    with open(configpath, 'rb') as f:
        config = tomli.load(f)
    config_github = config['API']['Github']

    # Init Github API
    github_ = Github(config_github)

    # Get last commit
    github_.get_last_commit_date()


if __name__ == '__main__':
    main()
