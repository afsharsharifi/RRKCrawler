# RRK Crawler

## Table of Contents

* [Overview](#overview)
* [Tech Stack](#tech-stack)
* [How to Run](#how-to-run)
* [Project Structure](#project-structure)

---

## Overview

This project implements a service that performs **scraping from rrk.ir**, extracts structured data.

---

## Tech Stack

* **Python:** 3.14.0
* **Framework:** Selenium, Requests

---

## How to Run

```bash
virtualenv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Run 
```bash
python main.py
```

---

---

**Sample Response:**

```json
[
    [
        "030817956753660",
        " آگهي ثبت تغيير شركت سهامي خاص بهينه ساز خودرو شرق توس به شماره ثبت 43964 و شناسه ملی 10380597837",
        "1403/08/16",
        "102",
        "23522",
        "1404/10/04",
        "140330406185020680",
        "10380597837",
        "آگهي تغييرات شركت سهامي خاص بهينه ساز خودرو شرق توس به شناسه ملي 10380597837 و به شماره ثبت 43964 به استناد صورتجلسه مجمع عمومي عادي بطور فوق العاده مورخ 13/08/1403 تصميمات ذيل اتخاذ شد خانم منصوره مح....",
        "<a  href=\"/ords/r/rrs/rrs-front/f-detail-ad?p28_code=18077851&p28_from_page=199&clear=28&session=8651876865011&cs=3-H-16Zpa4n-Y1B3StNlraJF5dW3hoOmeC_WDVqnTI3I3_YV300O7NoGj70B8VkhxQANKN3GAQxTsNCUAQASCRw\" ><img src=\"r/rrs/200/files/static/v1410/Attachment.png\" class=\"apex-edit-pencil\" border=\"0\"></a>",
        "<button  href=\"/ords/r/rrs/rrs-front/f-detail-ad?p28_code=18077851&p28_from_page=199&clear=28&session=8651876865011&cs=3-H-16Zpa4n-Y1B3StNlraJF5dW3hoOmeC_WDVqnTI3I3_YV300O7NoGj70B8VkhxQANKN3GAQxTsNCUAQASCRw\" >مشاهده جزئیات آگهی</button>",
        "انتشار یافته امضا شده",
        {
            "v": "4",
            "d": "شهرستان"
        },
        "23/12/2025",
        " آگهي ثبت تغيير شركت سهامي خاص بهينه ساز خودرو شرق توس به شماره ثبت 43964 و شناسه ملی 10380597837",
        {
            "salt": "oNJdrgMozhI0DN6SZLNHdw",
            "protected": "/ZBy9NKvZp47sf4L8PduIL6hJcndgHWQwEYBRZ-Z7n-WCfa4e2jwLaCQ6_pxx5GRZmjlZQe2_83J9OJcqnwj8CA",
            "rowVersion": "OW6mK1YkJkAPsDODOKi7_rYeaq9ahBrKQmIMMVGRAGLm8GoL3T9IcNg3ZUXVL8TmH5hCwdubgSUIvSmbuqSUdw"
        }
    ],
    ...
]
```

## Project Structure

```text
RRKCrawler/
├── crawler/
│   ├── base_session.py
│   ├── config.py
│   └── utils.py
├── .gitignore
├── app.py
├── main.py
├── requirements.txt
└── README.md
```