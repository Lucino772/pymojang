from __future__ import annotations

import inspect
import json
from typing import TYPE_CHECKING

from mojang.exceptions import MethodNotAllowed, NotFound, ServerError

if TYPE_CHECKING:
    import requests


def get_headers(json_content: bool | None = False, bearer: str | None = None):
    headers = {}

    if json_content:
        headers["content-type"] = "application/json"
        headers["accept"] = "application/json"

    if bearer:
        headers["authorization"] = f"Bearer {bearer}"

    return headers


def err_check(response: requests.Response, *args, use_defaults: bool | None = True):
    if use_defaults:
        args += ((404, NotFound), (405, MethodNotAllowed), (500, ServerError))

    status_code = response.status_code
    for codes, exception in args:
        do_raise = (isinstance(codes, list) and status_code in codes) or (
            isinstance(codes, int) and status_code == codes
        )

        if do_raise and inspect.isclass(exception):
            raise exception(response.text)
        if do_raise:
            raise exception

    data = None
    try:
        data = response.json()
    except json.decoder.JSONDecodeError:
        data = response.text

    return status_code, data
