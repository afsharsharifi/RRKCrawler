"""_summary_"""

import json
import logging
import time
from urllib.parse import parse_qs, unquote

import jdatetime
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumwire import webdriver


class BaseSession:
    """Getting rrk.ir Session Information"""

    def __init__(self, headless: bool = True, days: int = 10, sleep: int = 12):
        """_summary_"""
        self.driver = None
        self.target_url = "https://rrk.ir/ords/r/rrs/rrs-front/داده-باز"
        self.headless = headless
        self.days = days
        self.sleep = sleep

    def _build_options(self):
        """_summary_"""
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36")
        options.add_argument("--accept-lang=en-US,en")
        return options

    def start_driver(self):
        """_summary_"""
        options = self._build_options()
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.target_url)

    def stop_driver(self):
        """_summary_"""
        if self.driver:
            self.driver.quit()

    def last_n_days_range(self):
        """_summary_"""
        today = jdatetime.date.today()
        start_date = today - jdatetime.timedelta(days=self.days - 1)
        return (start_date.strftime("%Y/%m/%d"), today.strftime("%Y/%m/%d"))

    def submit_date_range(self):
        """_summary_"""
        date_from, date_to = self.last_n_days_range()
        self.driver.find_element(By.ID, "P199_NEWSPAPERDATE_AZ").send_keys(date_from)
        self.driver.find_element(By.ID, "P199_NEWSPAPER_TA").send_keys(date_to)
        self.driver.find_element(By.ID, "B912476867105247978").click()

    def wait_for_response(self):
        """_summary_"""
        logging.info("Going to sleep for 10 seconds")
        time.sleep(self.sleep)
        logging.info("Awake")

    def chnage_body_settings(self, dict_body: dict):
        """_summary_"""
        chnaged = dict_body
        chnaged["p_json"][0]["regions"][0]["fetchData"]["maxRows"] = 1000
        return chnaged

    def parse_cookie_header(self, cookie_str):
        """_summary_"""
        cookies = {}
        for part in cookie_str.split(";"):
            if "=" in part:
                k, v = part.strip().split("=", 1)
                cookies[k] = v
        return cookies

    def extract_body(self):
        """_summary_"""
        for request in self.driver.requests:
            if "https://rrk.ir/ords/wwv_flow.ajax?p_context=rrs-front" in request.url and request.method == "POST":
                raw_body = request.body.decode("utf-8")
                parsed = parse_qs(raw_body)
                if "p_json" not in parsed:
                    return None
                p_json_decoded = unquote(parsed["p_json"][0])
                data = json.loads(p_json_decoded)
                if "regions" in data:
                    parsed["p_json"][0] = data
                    chnaged_body = self.chnage_body_settings(parsed)
                    cookie = self.parse_cookie_header(request.headers.get("Cookie", None))
                    return {
                        "body": chnaged_body,
                        "cookie": cookie,
                        "header": request.headers,
                        "url": request.url,
                    }
        return None

    def run(self):
        """_summary_"""
        self.start_driver()
        self.submit_date_range()
        self.wait_for_response()
        response = self.extract_body()
        self.stop_driver()
        return response


def main():
    """_summary_"""
    base_session = BaseSession(headless=False, sleep=15)
    settings = base_session.run()
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
    print(response.json())
    # data = response.json()
    # with open("response.json", "w", encoding="utf-8") as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
