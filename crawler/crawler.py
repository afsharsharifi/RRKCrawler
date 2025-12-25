"""_summary_"""

import json
import time
from urllib.parse import parse_qs, unquote

import jdatetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumwire import webdriver


class BrowserConfig:
    """Handles Selenium WebDriver configuration."""

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"

    @staticmethod
    def create_driver() -> webdriver.Chrome:
        """_summary_"""
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={BrowserConfig.USER_AGENT}")
        options.add_argument("--accept-lang=en-US,en")

        return webdriver.Chrome(options=options)


class DateUtils:
    """Utility methods for Jalali date handling."""

    @staticmethod
    def last_days(days: int) -> tuple[str, str]:
        """_summary_"""
        today = jdatetime.date.today()
        start_date = today - jdatetime.timedelta(days=days - 1)
        return (start_date.strftime("%Y/%m/%d"), today.strftime("%Y/%m/%d"))


class AjaxRequestParser:
    """Parses Ajax POST requests and extracts required payload."""

    @staticmethod
    def extract_serialized_data(raw_body: bytes) -> dict | None:
        """_summary_"""
        decoded_body = raw_body.decode("utf-8")
        parsed_body = parse_qs(decoded_body)

        if "p_json" not in parsed_body:
            return None

        json_payload = unquote(parsed_body["p_json"][0])
        data = json.loads(json_payload)

        if "regions" not in data:
            return None

        region = data["regions"][0]

        return {
            "report_id": region.get("reportId"),
            "ajax_columns": region.get("ajaxColumns"),
            "id": region.get("id"),
            "ajax_identifier": region.get("ajaxIdentifier"),
            "protected": data.get("pageItems", {}).get("protected"),
            "salt": data.get("salt"),
        }


class RRKScraper:
    """Main scraper class for rrk.ir."""

    BASE_URL = "https://rrk.ir/ords/r/rrs/rrs-front/داده-باز"
    AJAX_URL_KEYWORD = "https://rrk.ir/ords/wwv_flow.ajax?p_context=rrs-front"

    def __init__(self, days: int = 10, wait_seconds: int = 12):
        self.days = days
        self.wait_seconds = wait_seconds
        self.driver = BrowserConfig.create_driver()

    def open_page(self) -> None:
        """_summary_"""
        self.driver.get(self.BASE_URL)

    def apply_date_filter(self) -> None:
        """_summary_"""
        from_date, to_date = DateUtils.last_days(self.days)

        self.driver.find_element(By.ID, "P199_NEWSPAPERDATE_AZ").send_keys(from_date)
        self.driver.find_element(By.ID, "P199_NEWSPAPER_TA").send_keys(to_date)
        self.driver.find_element(By.ID, "B912476867105247978").click()

    def wait_for_requests(self) -> None:
        """_summary_"""
        print(f"Sleeping for {self.wait_seconds} seconds...")
        time.sleep(self.wait_seconds)
        print("Awake!")

    def extract_ajax_data(self) -> dict | None:
        """_summary_"""
        for request in self.driver.requests:
            if self.AJAX_URL_KEYWORD in request.url and request.method == "POST" and request.body:
                result = AjaxRequestParser.extract_serialized_data(request.body)
                if result:
                    return {"session": result, "cookie": request.headers.get("Cookie", None)}
        return None

    def run(self) -> dict | None:
        """_summary_"""
        try:
            self.open_page()
            self.apply_date_filter()
            self.wait_for_requests()
            return self.extract_ajax_data()
        finally:
            self.driver.quit()
