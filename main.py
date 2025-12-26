"""_summary_"""

import json
from functools import wraps
from time import time

import requests

from crawler.base_session import BaseSession


def timing(f):
    """_summary_"""

    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f()
        te = time()
        print("took: %2.4f sec" % (te - ts))
        return result

    return wrap


@timing
def main():
    """_summary_"""
    base_session = BaseSession(headless=False, sleep=15)
    settings = base_session.run()

    if not settings:
        print("No data extracted from session.")
        return

    session = requests.Session()
    session.headers.update(settings["header"])
    session.cookies.update(settings["cookie"])

    converted = {
        "p_flow_id": settings["body"]["p_flow_id"][0],
        "p_flow_step_id": settings["body"]["p_flow_step_id"][0],
        "p_instance": settings["body"]["p_instance"][0],
        "p_debug": "",
        "p_json": json.dumps(settings["body"]["p_json"][0], ensure_ascii=False),
    }

    response = session.post(settings["url"], data=converted, verify=False)
    data = response.json()

    with open("response.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Total Papers: ", data["regions"][0]["fetchedData"]["totalRows"])
    print("Response saved to response.json")


if __name__ == "__main__":
    main()
