"""summery"""

import json
from typing import Any

import requests

from crawler.crawler import RRKScraper

crawler = RRKScraper(days=10, wait_seconds=12)
settings = crawler.run()


class RRKSession:
    """Manages HTTP session, headers, and cookies."""

    BASE_HEADERS = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://rrk.ir",
        "Referer": "https://rrk.ir/",
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) " "AppleWebKit/537.36 (KHTML, like Gecko) " "Chrome/142.0.0.0 Safari/537.36"),
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    BASE_COOKIES = {
        "ORA_WWV_APP_200": settings["cookie"]["ORA_WWV_APP_200"],
        "cookiesession1": settings["cookie"]["cookiesession1"],
    }

    @staticmethod
    def create() -> requests.Session:
        """_summary_"""
        session = requests.Session()
        session.headers.update(RRKSession.BASE_HEADERS)
        session.cookies.update(RRKSession.BASE_COOKIES)
        return session


class RRKAjaxClient:
    """Handles Ajax POST requests to rrk.ir."""

    AJAX_URL = f"https://rrk.ir/ords/wwv_flow.ajax?p_context=rrs-front/داده-باز/{settings[""]}"

    def __init__(self, session: requests.Session):
        self.session = session

    def post(self, payload: dict) -> dict[str, Any]:
        """_summary_"""
        response = self.session.post(
            self.AJAX_URL,
            data=payload,
            verify=False,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


class JsonFileWriter:
    """Writes JSON data to disk."""

    @staticmethod
    def write(filename: str, data: dict) -> None:
        """_summary_"""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


class RRKService:
    """Facade service for fetching and saving RRK Ajax data."""

    def __init__(self, payload: dict):
        self.payload = payload
        self.session = RRKSession.create()
        self.client = RRKAjaxClient(self.session)

    def fetch(self) -> dict:
        """_summary_"""
        return self.client.post(self.payload)

    def fetch_and_save(self, filename: str) -> dict:
        """_summary_"""
        data = self.fetch()
        JsonFileWriter.write(filename, data)
        return data


def main():
    """_summary_"""
    payload = {
        "p_flow_id": "200",
        "p_flow_step_id": "199",
        "p_instance": "13640361552939",
        "p_debug": "",
        "p_json": """{
            "regions": [
                {
                    "reportId": "1115937865841778825",
                    "view": "grid",
                    "ajaxColumns": "MTA4MzczMDM0MjI3MTk1NTUxMDoxMDgzNzMwNDMyNTc4OTU1NTEx...",
                    "id": "1083730177584955508",
                    "ajaxIdentifier": "UkVHSU9OIFRZUEV-fjEwODM3MzAxNzc1ODQ5NTU1MDg/...",
                    "fetchData": {
                        "version": 1,
                        "firstRow": 1,
                        "maxRows": 1000
                    }
                }
            ],
            "pageItems": {
                "itemsToSubmit": [
                    {"n": "P199_SABTNODATE_AZ", "v": "1404/10/03"},
                    {"n": "P199_SABTNODATE_TA", "v": "1404/10/03"}
                ],
                "protected": "UDBfQ1VSUkVOVF9QQUdFX0lEOlAw...",
                "rowVersion": "",
                "formRegionChecksums": []
            },
            "salt": "70099237277901894751768079060458179697"
        }""",
    }

    service = RRKService(payload)
    service.fetch_and_save("response.json")
    print("JSON با موفقیت ذخیره شد")


if __name__ == "__main__":
    main()
