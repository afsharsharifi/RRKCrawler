"""_summary_"""

import json

import requests

session = requests.Session()
session.headers.update(
    {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://rrk.ir",
        "Referer": "https://rrk.ir/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }
)
session.cookies.update(
    {
        "ORA_WWV_APP_200": "ORA_WWV-BKMfvnmAtzu3TKx0TWG6tjP2",
        "cookiesession1": "678ADA59FA7420AB332506D18C9E6869",
    }
)

response = session.post(
    "https://rrk.ir/ords/wwv_flow.ajax?p_context=rrs-front/داده-باز/13640361552939",
    data={
        "p_flow_id": "200",
        "p_flow_step_id": "199",
        "p_instance": "13640361552939",
        "p_debug": "",
        "p_json": """{
        "regions":[
            {
                "reportId":"1115937865841778825",
                "view":"grid",
                "ajaxColumns":"MTA4MzczMDM0MjI3MTk1NTUxMDoxMDgzNzMwNDMyNTc4OTU1NTExOjEwODM3MzA1.,OTA0MTg5NTU1MTI6MTA4MzczMDc1NTUwMjk1NTUxNDoxMDgzNzMwODk0OTE0OTU1.,NTE1OjEwODM3MzA5Mzg0OTc5NTU1MTY6MTA4MzczMTA2NTM1MTk1NTUxNzoxMDgz.,NzMxMTk4NjMyOTU1NTE4OjEwODM3MzEyNDg0MDQ5NTU1MTk6MTA4MzczMTM0ODIx.,Njk1NTUyMDoxMDgzNzMxNDUzMzA3OTU1NTIxOjEwODM3MzE1NDc1ODY5NTU1MjI6.,MTA4MzczMTY1ODI0Mzk1NTUyMzoxMDgzNzMxNzg5NDc3OTU1NTI0OjE0MjY4MTAw.,MjM1NzU1MjY1MDY/_65hL9xS-f9FOJYIWs47l6qWXYcQPf2HnFqAkwuNaw6rxt-PeBRtlk2SRhqiFiucmN_BpCeVADNZh18ZIknXNA",
                "id":"1083730177584955508",
                "ajaxIdentifier":"UkVHSU9OIFRZUEV-fjEwODM3MzAxNzc1ODQ5NTU1MDg/yuk74q8J_4OZog1t_ETkPbp7cGte2oVPKtQSI12paKa47DN_obGj1OgGghf2z8a5hd4CR0vv5m6U20nnuniHEg",
                "fetchData":{
                    "version":1,
                    "firstRow":1,
                    "maxRows":1000
                }
            }
        ],
        "pageItems":{
            "itemsToSubmit":[
                {"n":"P199_COMPANY_NAME","v":""},
                {"n":"P199_NATIONALCODECOMPANY","v":""},
                {"n":"P199_SABTNOCOMPANY","v":""},
                {"n":"P199_NOE_AGAHI","v":""},
                {"n":"P199_INDIKATORNUMBER","v":""},
                {"n":"P199_NEWSPAPERTYPE","v":""},
                {"n":"P199_NEWSPAPERNO","v":""},
                {"n":"P199_PAGENUMBER","v":""},
                {"n":"P199_CODEPEYGIRI","v":""},
                {"n":"P199_EZHARNAMEHNO","v":""},
                {"n":"P199_CITYCODE","v":""},
                {"n":"P199_SABTNODATE_AZ","v":"1404/10/03"},
                {"n":"P199_SABTNODATE_TA","v":"1404/10/03"},
                {"n":"P199_NEWSSTATUS","v":""},
                {"n":"P199_NEWSPAPERDATE_AZ","v":""},
                {"n":"P199_NEWSPAPER_TA","v":""}
            ],
            "protected":"UDBfQ1VSUkVOVF9QQUdFX0lEOlAwX09SREVSX0lEOlAwX1RPT0xUSVBfQkFOTkVS/mbMIwwIfYdYgqJNOBjEyvFbyULfaBS_Xy4BJKoJ6OvZgVeMygqwxM_e6F1kyWWzvIxHRW9SRa_TFiDgihnX2qg",
            "rowVersion":"",
            "formRegionChecksums":[]
        },
        "salt":"70099237277901894751768079060458179697"
    }""",
    },
    verify=False,
)

data = response.json()

with open("response.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("JSON با موفقیت ذخیره شد")
