from typing import Optional


def get_headers(
    json_content: Optional[bool] = False, bearer: Optional[str] = None
):
    headers = {}

    if json_content:
        headers["content-type"] = "application/json"
        headers["accept"] = "application/json"

    if bearer:
        headers["authorization"] = f"Bearer {bearer}"
