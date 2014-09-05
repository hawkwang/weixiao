# -*- coding: utf-8 -*-
import scrapy


class EventSpider(scrapy.Spider):
    name = "event"
    allowed_domains = ["http://www.cnccchina.com"]
    start_urls = (
        'http://www.http://www.cnccchina.com/',
    )

    def parse(self, response):
        pass
