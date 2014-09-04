import urlparse

from scrapy import log
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from douban.items import DoubanItem
import sys
import re
import redis

def UrlChecker(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.match(url):
        return True
    return False
#end def

def isTargetPage(targetpattern, url):
    regex = re.compile(targetpattern, re.IGNORECASE)
    if(regex.match(url)):
        return True
    return False
#end def


class DoubanSpider(CrawlSpider):
    """ General configuration of the Crawl Spider """
    name = 'douban'
    allowed_domains = ["mosh.cn"]
    #allowed_domains = ["www.douban.com"]
    #start_urls = ['http://shanghai.douban.com/events/week-all','http://beijing.douban.com/events/week-all'] # urls from which the spider will start crawling
    start_urls = ['http://www.mosh.cn'] # urls from which the spider will start crawling
    rules = ()
    targetpattern = r'http://www.mosh.cn/events/\d+'
    
    redis = redis.StrictRedis(host='localhost', port=6379, db=0)


    def __init__(self, name=None, **kwargs):
        super(DoubanSpider, self).__init__(name, **kwargs)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.items_buffer = {}
        #self.base_url = "http://chinaticket.com"
        from scrapy.conf import settings
        settings.overrides['DOWNLOAD_TIMEOUT'] = 3600
    #end def

    def isNewUrl(self, url):
        if self.redis.get(url)==None :
            self.redis.set(url,1)
            return True
        else:
            return False
        #end if
    #end def

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        #log.msg("Parsing for URL {%s}"%format(response.request.url))
        links = hxs.select('//a/@href')
        for link in links:
            v_url = ''.join( link.extract() )
            if (not v_url) or (UrlChecker(v_url)==False):
                continue
            else:
                if isTargetPage(self.targetpattern,v_url) and self.isNewUrl(v_url)==True :
                    yield Request( url=v_url, callback=self.parse_details)
                    continue    
                #end if
                #log.msg("Getting link URL %s" % format(v_url))
                yield Request( url=v_url, callback=self.parse )
            #end if
        #end for
    #end def

    def parse_details(self, response):
        print '[weixiao] Start scrapping detailed info ...'
        #log.msg("Parsing detailed info for URL - %s" % format(response.request.url))
        hxs = HtmlXPathSelector(response)
        title = hxs.xpath('//*[@id="collectinfo"]/text()').extract()[0]
        print '[weixiao] title - %s' % title
    #end def


