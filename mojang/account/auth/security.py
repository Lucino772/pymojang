from typing import List

import requests

from ...exceptions import *
from ..structures.auth import ChallengeInfo
from ..utils.auth import BearerAuth, URLs


def check_ip(access_token: str) -> bool:
    """Check if authenticated user IP is secure
    
    Args:
        access_token (str): The session's access token
    
    Returns:
        True if IP is secure else False
    
    Raises:
        Unauthorized: If access token is invalid
        PayloadError: If access token is not formated correctly
    """
    response = requests.get(URLs.verify_ip(), auth=BearerAuth(access_token))
    try:
        handle_response(response, PayloadError, Unauthorized, IPNotSecured)
    except IPNotSecured:
        return False
    else:
        return True

def get_challenges(access_token: str) -> List[ChallengeInfo]:
    """Return a list of challenges to verify IP
    
    Args:
        access_token (str): The session's access token
    
    Returns:
        A list of ChallengeInfo
    
    Example:
        
        Example of challenges
        ```python
        [
            (123, "What is your favorite pet's name?"),
            (456, "What is your favorite movie?"),
            (789, "What is your favorite author's last name?")
        ]
        ```
    
    Raises:
        Unauthorized: If access token is invalid
        PayloadError: If access token is not formated correctly
    """
    response = requests.get(URLs.get_challenges(), auth=BearerAuth(access_token))
    data = handle_response(response, PayloadError, Unauthorized)

    _challenges = []
    for item in data:
        _challenges.append(ChallengeInfo(id=item['answer']['id'], challenge=item['question']['question']))

    return _challenges

def verify_ip(access_token: str, answers: list) -> bool:
    """Verify IP with the given answers
    
    Args:
        access_token (str): The session's access token
        answers (list): The answers to the question
    
    Example:
        
        ```python
        answers = [
            (123, "foo"),
            (456, "bar"),
            (789, "baz")
        ]
        security.verify_user_ip(ACCESS_TOKEN, answers)
        ```
    
    Returns:
        True if IP is secure else False
    
    Raises:
        Unauthorized: If access token is invalid
        PayloadError: If access token is not formated correctly
    """
    answers = list(map(lambda a: {'id': a[0], 'answer': a[1]}, answers))
    response = requests.post(URLs.verify_ip(), auth=BearerAuth(access_token), json=answers)
    try:
        handle_response(response, PayloadError, Unauthorized, IPVerificationError)
    except IPVerificationError:
        return False
    else:
        return True
