# coding: utf-8
import os.path
import pickle
import requests
import time

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleCalendar(object):

    def __init__(self, token_file=None, credentials_file=None):
        self.scopes = ['https://www.googleapis.com/auth/calendar.readonly']
        self.token_file = token_file or 'token.pickle'
        self.credentials_file = credentials_file or 'credentials.json'
        self._credentials = None
        self._flow = None

        self.refresh_token()

    @property
    def credentials(self):
        if self._credentials:
            return self._credentials

        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self._credentials = pickle.load(token)
                return self._credentials
        else:
            return None

    @credentials.setter
    def credentials(self, credentials):
        self._credentials = credentials
        with open(self.token_file, 'wb') as token:
            pickle.dump(credentials, token)

    @property
    def is_authenticated(self):
        return (self.credentials and self.credentials.valid)

    @property
    def flow(self):
        if not self._flow:
            self._flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
        return self._flow

    def get_device_code(self):
        req = requests.post('https://accounts.google.com/o/oauth2/device/code',
                            params={'client_id': self.flow.client_config['client_id'],
                                    'scope': self.scopes[0]},
                            headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if req.status_code == 200:
            self.device = req.json()
            return req.json()
        else:
            return False

    def wait_fetch_token(self):
        while True:
            try:
                # Dirty hack to set grant_type
                self.flow.oauth2session._client.grant_type = 'http://oauth.net/grant_type/device/1.0'

                self.flow.fetch_token(code=self.device['device_code'])
                self.credentials = self.flow.credentials
                break
            except Exception:
                time.sleep(2)

    def refresh_token(self):
        if self.credentials and self.credentials.expired and self.credentials.refresh_token:
            self.credentials.refresh(Request())


b = GoogleCalendar()
if not b.is_authenticated:
    device = b.get_device_code()
    print('Go to {} and enter {}'.format(device['verification_url'], device['user_code']))
    b.wait_fetch_token()

if b.is_authenticated:
    print('Great Success')
