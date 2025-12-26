import time

import jdatetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from .config import TARGET_URL, USER_AGENT
from .utils import change_body_settings, decode_request_body, parse_cookie_header


class BaseSession:
    """Manage Selenium session and extract request data."""

    def __init__(self, headless: bool = True, days: int = 10, sleep: int = 12):
        self.driver = None
        self.headless = headless
        self.days = days
        self.sleep = sleep

    def _build_options(self) -> Options:
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={USER_AGENT}")
        options.add_argument("--accept-lang=en-US,en")
        return options

    def start_driver(self):
        """start the driver with _build_options"""
        self.driver = webdriver.Chrome(options=self._build_options())
        self.driver.get(TARGET_URL)

    def stop_driver(self):
        """stop the driver"""
        if self.driver:
            self.driver.quit()

    def last_n_days_range(self) -> tuple[str, str]:
        """
        Returns:
            tuple[str, str]: from_date, to_date (today)
        """
        today = jdatetime.date.today()
        start_date = today - jdatetime.timedelta(days=self.days - 1)
        return start_date.strftime("%Y/%m/%d"), today.strftime("%Y/%m/%d")

    def submit_date_range(self):
        """set search form input values and submit"""
        date_from, date_to = self.last_n_days_range()
        self.driver.find_element(By.ID, "P199_NEWSPAPERDATE_AZ").send_keys(date_from)
        self.driver.find_element(By.ID, "P199_NEWSPAPER_TA").send_keys(date_to)
        self.driver.find_element(By.ID, "B912476867105247978").click()

    def wait_for_response(self):
        """sleep for gived time in __init__"""
        time.sleep(self.sleep)

    def extract_body(self) -> dict | None:
        """
        Returns:
            dict | None: serialized body, cookie, header
        """
        for request in self.driver.requests:
            if "https://rrk.ir/ords/wwv_flow.ajax?p_context=rrs-front" in request.url and request.method == "POST":
                parsed = decode_request_body(request.body)
                if not parsed or "regions" not in parsed["p_json"][0]:
                    continue
                chnaged_body = change_body_settings(parsed)
                cookie = parse_cookie_header(request.headers.get("Cookie", None))
                return {
                    "body": chnaged_body,
                    "cookie": cookie,
                    "header": request.headers,
                    "url": request.url,
                }
        return None

    def run(self) -> dict | None:
        """
        Returns:
            dict | None: serialized body, cookie, header
        """
        self.start_driver()
        self.submit_date_range()
        self.wait_for_response()
        result = self.extract_body()
        self.stop_driver()
        return result
