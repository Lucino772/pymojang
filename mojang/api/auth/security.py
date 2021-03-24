from ...error.exceptions import *
from ...utils import web
from ..urls import SECURITY_CHALLENGES, SECURITY_CHECK


def is_user_ip_secure(access_token: str) -> bool:
    try:
        web.auth_request('get', SECURITY_CHECK, access_token, exceptions=(PayloadError, Unauthorized, IPNotSecured))
    except IPNotSecured:
        return False
    else:
        return True

def get_user_challenges(access_token: str) -> list:
    data = web.auth_request('get', SECURITY_CHALLENGES, access_token, exceptions=(PayloadError, Unauthorized))
    challenges = []
    if data:
        for item in data:
            answer_id = item['answer']['id']
            question = item['question']['question']
            challenges.append((answer_id, question))
        return challenges

def verify_user_ip(access_token: str, answers: list) -> bool:
    formatted_answers = []
    for answer in answers:
        formatted_answers.append({
            'id': answer[0],
            'answer': answer[1]
        })
    try:
        web.auth_request('post', SECURITY_CHECK, access_token, exceptions=(PayloadError, Unauthorized, IPVerificationError), json=formatted_answers)
    except IPVerificationError:
        return False
    else:
        return True
