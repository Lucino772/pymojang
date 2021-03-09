import requests
import json
from urllib.parse import urljoin

class SecurityCheck:

    ROOT_URL = 'https://api.mojang.com/user/security/'

    def __init__(self, session: requests.Session):
        self._session = session

    @property
    def ok(self):
        check_url = urljoin(self.ROOT_URL, 'location')
        response = self._session.get(check_url)
        return response.status_code == 204
    
    @property
    def challenges(self):
        challenges_url = urljoin(self.ROOT_URL, 'challenges')
        response = self._session.get(challenges_url)
        return response.json()

    def send_answers(self, answers: list):
        answers_url = urljoin(self.ROOT_URL, 'location')
        response = self._session.post(answers_url, json=answers)
        return response.status_code == 204

    