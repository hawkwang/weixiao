#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
import sys     # 1
import hashlib
#from weixiao.items import WeixiaoItem
#from weixiao.pipelines import to_unicode_or_bust, validate_time, validate_date


# pattern example : http://www.clcn.net.cn/modules/events/index.php?cat_id=4&start=0
def getUrls():
    urls = []
    baseUrl = 'http://www.clcn.net.cn/modules/events/index.php?'
    for category in range(1,16):
        url1 = baseUrl + 'cat_id=' + str(category)
        for i in range(0,11):
            url = url1 + '&start=' + str(i*10)
            urls.append(url) 
        #end for
    #end for
    
    return urls
#end def


class EventSpider(CrawlSpider):
    name = "event"
    allowed_domains = ["www.clcn.net.cn"]
    start_urls = getUrls()
    rules = ()
    baseurl = 'http://www.clcn.net.cn/modules/events/'

    def __init__(self, name=None, **kwargs):
        super(EventSpider, self).__init__(name, **kwargs)

        reload(sys)
        sys.setdefaultencoding('utf-8') 

    #end def

    def parse(self, response):
        #print '[weixiao] - processing ' + response.request.url
        try:
            hxs = HtmlXPathSelector(response)
            links = hxs.select('//div[@class="cultrue_content_list"]/ul//a/@href')
            if not links:
                return
            #end if
            for link in links:
                v_url = ''.join( link.extract() )
                if not v_url:
                    continue
                else:
                    #print "[weixiao] sending low level url - ", self.baseurl + v_url
                    yield Request( url = self.baseurl+v_url, callback=self.parse_details )
            #end for
        except Exception as e:
            raise

        #end try-except
    #end def

    def parse_details(self, response):
        print "[weixiao] Start scrapping Detailed Info...."
        try:
            hxs = HtmlXPathSelector(response)
            title = hxs.xpath('//*[@id="events_info"]/h3/text()').extract()[0].strip()
            print title
        except Exception as e:
            raise
        #end try-except
    #end def

#end class
