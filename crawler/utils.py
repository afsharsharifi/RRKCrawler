"""_summary_"""

import json
from urllib.parse import parse_qs, unquote


def parse_cookie_header(cookie_str: str) -> dict:
    """Parse cookie string into dictionary."""
    cookies = {}
    if not cookie_str:
        return cookies
    for part in cookie_str.split(";"):
        if "=" in part:
            k, v = part.strip().split("=", 1)
            cookies[k] = v
    return cookies


def change_body_settings(dict_body: dict) -> dict:
    """Modify body settings (maxRows) before sending request."""
    dict_body["p_json"][0]["regions"][0]["fetchData"]["maxRows"] = 1000
    return dict_body


def decode_request_body(raw_body: bytes) -> dict:
    """Decode POST request body and return JSON data."""
    parsed = parse_qs(raw_body.decode("utf-8"))
    if "p_json" not in parsed:
        return None
    p_json_decoded = unquote(parsed["p_json"][0])
    data = json.loads(p_json_decoded)
    parsed["p_json"][0] = data
    return parsed
