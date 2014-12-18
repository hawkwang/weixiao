# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


class WeixiaoItem(Item):
    # define the fields for your item here like:
    md5                 = Field()
    source              = Field()
    city		= Field()
    category	        = Field()
    detailedCategory	= Field()
    title		= Field()
    link		= Field()
    date		= Field()
    time		= Field()
    place		= Field()
    fee			= Field()
    feelist             = Field()
    image               = Field()
    desc		= Field()
    status              = Field()
    created             = Field()
#end class
