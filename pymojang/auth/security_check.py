import requests
from ..urls import MOJANG_API

class SecurityCheck:

    def __init__(self, session: requests.Session):
        self._session = session

    @property
    def ok(self):
        check_url = MOJANG_API.join('user/security/location')
        response = self._session.get(check_url)
        return response.status_code == 204
    
    @property
    def challenges(self):
        challenges_url = MOJANG_API.join('user/security/challenges')
        response = self._session.get(challenges_url)
        return response.json()

    def send_answers(self, answers: list):
        answers_url = MOJANG_API.join('user/security/location')
        response = self._session.post(answers_url, json=answers)
        return response.status_code == 204

    