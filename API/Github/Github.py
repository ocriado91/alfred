#!/usr/bin/env python3

from API.API_abstract import API
import github
import toml
import sys


class Github(API):
    ''' Wrapper Github class of PyGithub '''
    def __init__(self,
                 config: dict):

        github_api_key = config['API']['Github']['API_KEY']
        self.github = github.Github(github_api_key)
        self.get_last_commit_date()

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

    def show_options(self):
        message = 'Please select and option:\n'
        message += ' 1) Show last commit\n'
        return message

    def process_action(self,
                       message: str,
                       retry: int):
        logger.info(f'Trying to process {message} at try = {self.entry}')
        


def main():

    configpath = sys.argv[1]
    config = toml.load(configpath)
    config_github = config['API']['Github']

    # Init Github API
    github = Github(config_github)

    # Get last commit
    github.get_last_commit_date()


if __name__ == '__main__':
    main()
