from ...error.exceptions import *
from ...utils import web
from ..urls import SECURITY_CHALLENGES, SECURITY_CHECK


def is_user_ip_secure(access_token: str) -> bool:
    """Check if authenticated user IP is secure

    Args:
        access_token (str): The session's access token

    Returns:
        True if IP is secure else False

    Raises:
        Unauthorized: If access token is invalid
        PayloadError: If access token is not formated correctly
    """
    try:
        web.auth_request('get', SECURITY_CHECK, access_token, exceptions=(PayloadError, Unauthorized, IPNotSecured))
    except IPNotSecured:
        return False
    else:
        return True

def get_user_challenges(access_token: str) -> list:
    """Return a list of challenges to verify IP

    Args:
        access_token (str): The session's access token

    Returns:
        A list of tuples, each one contains the answer's id and the
        question

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
    data = web.auth_request('get', SECURITY_CHALLENGES, access_token, exceptions=(PayloadError, Unauthorized))
    challenges = []
    if data:
        for item in data:
            answer_id = item['answer']['id']
            question = item['question']['question']
            challenges.append((answer_id, question))
        return challenges

def verify_user_ip(access_token: str, answers: list) -> bool:
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
