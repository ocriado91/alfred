#!/usr/bin/env python3

import github

import toml
import sys


class Github:
    ''' Wrapper Github class of PyGithub '''
    def __init__(self,
                 config: dict):

        github_api_key = config['API_KEY']
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
