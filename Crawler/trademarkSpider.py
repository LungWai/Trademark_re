import json
# import math
# import bs4
import scrapy
from urllib.parse import urlencode
# from Jobs.items import JobItem, CompanyItem, JobDetailItem, MetaItem
# from utils import error_return_none


class JobsDBSpider(scrapy.Spider):
    name = "trademarkSpider"
    params = {"page":1, "rows":100}
    cookies = {"JSESSIONID":"141C8E96B6665947A666009F34F2C8A5",
               "XSRF-TOKEN":"07deedfd-6f37-4b7c-85d1-a3964ba75a3f",
               "_pk_id.1.998e":"b0e352443b219673.1705065155.",
               "GJ8UAX99J13WPQI51":"!barJA4+LffdkhPaMPnkppSQJxI0waSV0bXaRHybqzUowO4DtKWoBHYXKwwOH1aGjB4OTQfMbBcxu5bhDMo5s8MJz1wkjY540Ni3M6Wg=",
            #    "_pk_ref.1.998e":"%5B%22%22%2C%22%22%2C1708775127%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D",
               "_pk_ses.1.998e":"1"}
    id_page_url = "https://esearch.ipd.gov.hk/nis-pos-view/tm/search/"
    id_page_header = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Content-Type': 'application/json',
  'Cookie': 'XSRF-TOKEN=07deedfd-6f37-4b7c-85d1-a3964ba75a3f; JSESSIONID=141C8E96B6665947A666009F34F2C8A5; _pk_id.1.998e=b0e352443b219673.1705065155.; GJ8UAX99J13WPQI51=!barJA4+LffdkhPaMPnkppSQJxI0waSV0bXaRHybqzUowO4DtKWoBHYXKwwOH1aGjB4OTQfMbBcxu5bhDMo5s8MJz1wkjY540Ni3M6Wg=; _pk_ref.1.998e=%5B%22%22%2C%22%22%2C1708775127%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.1.998e=1',
  'Origin': 'https://esearch.ipd.gov.hk',
  'Pragma': 'no-cache',
  'Referer': 'https://esearch.ipd.gov.hk/nis-pos-view/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
  'X-XSRF-TOKEN': '07deedfd-6f37-4b7c-85d1-a3964ba75a3f',
  'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}






    # payload = json.dumps({
    #     "searchMethod": "TM_SEARCHMETHOD_WILDCARD",
    #     "tmText": "*",
    #     "filingDate": {},
    #     "documentFilingDate": {},
    #     "registrationDate": {},
    #     "isDeadRecordIndicator": "false",
    #     "expirationDate": {},
    #     "publicationDateOfAcceptance": {},
    #     "actualRegistrationDate": {}
    # })
    payload=json.dumps(
    {
    "searchMethod":"TM_SEARCHMETHOD_WILDCARD",
     "filingDate":{},
     "documentFilingDate":{},
     "applicationNumber":["*"],
     "registrationDate":{},
     "isDeadRecordIndicator":"false",
     "expirationDate":{},
     "publicationDateOfAcceptance":{},
     "actualRegistrationDate":{}
     })



    
    def __init__(self):
        super().__init__()

    def start_requests(self):
        yield scrapy.Request(method="POST", url=self.id_page_url + f"?{urlencode(self.params )}&", body=self.payload,
                             callback=self.parse_first_page, headers=self.id_page_header,)# cookies=self.cookies )

    def parse_first_page(self, response):
        yield from self.parse_page(response)
        total_page = int(response.json()["trademarks"]["totalPages"])

        for page in range(2, total_page):
            self.params.update({"page": page})
            yield scrapy.Request(method="POST", url=self.id_page_url + f"?{urlencode(self.params)}&", body=self.payload,
                                 callback=self.parse_page, headers=self.id_page_header,)# cookies=self.cookies)

    def parse_page(self, response):
        response_json = response.json()
        for item in response_json["trademarks"]["content"]:
            yield item