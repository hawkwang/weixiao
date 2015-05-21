# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeixiaoItem(scrapy.Item):
    # define the fields for your item here like:
    md5 = scrapy.Field()
    source = scrapy.Field()
    city = scrapy.Field()
    category = scrapy.Field()
    detailedCategory = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    place = scrapy.Field()
    fee = scrapy.Field()
    feelist = scrapy.Field()
    image = scrapy.Field()
    desc = scrapy.Field()
    status = scrapy.Field()
    created = scrapy.Field()
    #pass
