from typing import List

import requests

from ...exceptions import Unauthorized
from .. import helpers, urls
from ..structures import ChallengeInfo


def check_ip(access_token: str) -> bool:
    """Check if authenticated user IP is secure

    :param str access_token: The session's access token

    :raises Unauthorized: if access token is invalid
    :raises PayloadError: if access token is not formated correctly

    :Example:

    >>> from mojang.account.auth import security
    >>> security.check_ip('ACCESS_TOKEN')
    True
    """
    headers = helpers.get_headers(bearer=access_token)
    response = requests.get(urls.api_security_verify_ip, headers=headers)
    code, _ = helpers.err_check(
        response, (400, ValueError), (401, Unauthorized)
    )
    return code != 403


def get_challenges(access_token: str) -> List["ChallengeInfo"]:
    """Return a list of challenges to verify IP

    :param str access_token: The session's access token

    :raises Unauthorized: if access token is invalid
    :raises PayloadError: if access token is not formated correctly

    :Example:

    >>> from mojang.account.auth import security
    >>> security.get_challenges('ACCESS_TOKEN')
    [
        ChallengeInfo(id=123, challenge="What is your favorite pet's name?"),
        ChallengeInfo(id=456, challenge="What is your favorite movie?"),
        ChallengeInfo(id=589, challenge="What is your favorite author's last name?")
    ]
    """
    headers = helpers.get_headers(bearer=access_token)
    response = requests.get(urls.api_security_challenges, headers=headers)
    _, data = helpers.err_check(
        response, (400, ValueError), (401, Unauthorized)
    )

    _challenges = []
    for item in data:
        _challenges.append(
            ChallengeInfo(
                id=item["answer"]["id"], challenge=item["question"]["question"]
            )
        )

    return _challenges


def verify_ip(access_token: str, answers: list) -> bool:
    """Verify IP with the given answers

    :param str access_token: The session's access token
    :param list answers: The answers to the question

    :raises Unauthorized: if access token is invalid
    :raises PayloadError: if access token is not formated correctly

    :Example:

    >>> from mojang.account.auth import security
    >>> answers = [
    ...     (123, "foo"),
    ...     (456, "bar"),
    ...     (789, "baz")
    ... ]
    >>> security.verify_user_ip('ACCESS_TOKEN', answers)
    True
    """
    headers = helpers.get_headers(bearer=access_token)
    answers = list(map(lambda a: {"id": a[0], "answer": a[1]}, answers))
    response = requests.post(
        urls.api_security_verify_ip, headers=headers, json=answers
    )
    code, _ = helpers.err_check(
        response, (400, ValueError), (401, Unauthorized)
    )
    return code != 403
