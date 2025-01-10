#!/usr/bin/env python3

"""Base Class for all Google API services."""

import logging
import os.path
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class GoogleCommon:
    """Base Class for Google API services."""

    def get_credentials(
        self, configfile: str, scopes=list, service_name="tasks", version="v1"
    ):
        """Get Google Calendar credentials.

        The file token.pickle stores the user's access and refresh tokens,
        and is created automatically when the authorization flow completes
        for the first time.
        """
        logger.info("Reading configuration file from %s", configfile)
        creds = None
        token_path = os.path.join(configfile, "token.pickle")
        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            credentials = os.path.join(configfile, "client_secret.json")
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials, scopes
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, "wb") as token:
                pickle.dump(creds, token)

        self.service = build(service_name, version, credentials=creds)
