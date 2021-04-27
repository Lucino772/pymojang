import requests

from ._urls import URLs
from .._auth import BearerAuth
from .._structures import ChallengeInfo

# TODO: Handle errors and exception 

def check_ip(access_token: str):
    response = requests.get(URLs.verify_ip(), auth=BearerAuth(access_token))

def get_challenges(access_token: str):
    response = requests.get(URLs.get_challenges(), auth=BearerAuth(access_token))

    _challenges = []
    for item in response.json():
        _challenges.append(ChallengeInfo(id=item['answer']['id'], challenge=item['question']['question']))

    return _challenges

def verify_ip(access_token: str, answers: list):
    answers = map(lambda a: {'id': a[0], 'answer': a[1]}, answers)
    response = requests.post(URLs.verify_ip(), auth=BearerAuth(access_token), json=answers)
