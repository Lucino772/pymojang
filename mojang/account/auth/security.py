import requests

from ...exceptions import *
from .._auth import BearerAuth
from .._structures import ChallengeInfo
from ._urls import URLs


def check_ip(access_token: str):
    response = requests.get(URLs.verify_ip(), auth=BearerAuth(access_token))
    try:
        handle_response(response, PayloadError, Unauthorized, IPNotSecured)
    except IPNotSecured:
        return False
    else:
        return True

def get_challenges(access_token: str):
    response = requests.get(URLs.get_challenges(), auth=BearerAuth(access_token))
    data = handle_response(response, PayloadError, Unauthorized)

    _challenges = []
    for item in data:
        _challenges.append(ChallengeInfo(id=item['answer']['id'], challenge=item['question']['question']))

    return _challenges

def verify_ip(access_token: str, answers: list):
    answers = map(lambda a: {'id': a[0], 'answer': a[1]}, answers)
    response = requests.post(URLs.verify_ip(), auth=BearerAuth(access_token), json=answers)
    try:
        handle_response(response, PayloadError, Unauthorized, IPVerificationError)
    except IPVerificationError:
        return False
    else:
        return True
