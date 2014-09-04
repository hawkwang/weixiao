# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DoubanItem(Item):
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
    #pass
