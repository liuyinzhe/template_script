import scrapy
import asyncio

class Ja3Spider(scrapy.Spider):
    name = 'ja3'
    allowed_domains = ['ja3er.com']
    start_urls = ['https://ja3er.com/json']

    def start_requests(self):
        for _ in range(5):
            yield scrapy.Request(self.start_urls[0], callback=self.parse, dont_filter=True, meta={"ja3": True}) # 呐，只有这样才会调用特殊的下载逻辑

    def parse(self, response: scrapy.http.response.text.TextResponse):
        print(response.json())

import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
ASYNCIO_EVENT_LOOP = "asyncio.SelectorEventLoop"
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

DOWNLOAD_HANDLERS = {"https": "scrapy_unitest.handlers.Ja3DownloadHandler"}

