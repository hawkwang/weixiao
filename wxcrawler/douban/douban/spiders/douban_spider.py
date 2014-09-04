#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urlparse

from scrapy import log
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from douban.items import WeixiaoItem
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

def stripHTMLTags (html):
    """
      Strip HTML tags from any string and transfrom special entities
    """
    text = html
 
    # apply rules in given order!
    rules = [
        { r'>\s+' : u'>'},                  # remove spaces after a tag opens or closes
        { r'\s+' : u' '},                   # replace consecutive spaces
        { r'\s*<br\s*/?>\s*' : u'\n'},      # newline after a <br>
        { r'</(div)\s*>\s*' : u'\n'},       # newline after </p> and </div> and <h1/>...
        { r'</(p|h\d)\s*>\s*' : u'\n\n'},   # newline after </p> and </div> and <h1/>...
        { r'<head>.*<\s*(/head|body)[^>]*>' : u'' },     # remove <head> to </head>
        { r'<a\s+href="([^"]+)"[^>]*>.*</a>' : r'\1' },  # show links instead of texts
        { r'[ \t]*<[^<]*?/?>' : u'' },            # remove remaining tags
        { r'^\s+' : u'' }                   # remove spaces at the beginning
    ]
 
    for rule in rules:
        for (k,v) in rule.items():
            regex = re.compile (k)
            text  = regex.sub (v, text)
 
    # replace special strings
    special = {
        '&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"',
        '&lt;'   : '<', '&gt;'  : '>'
    }
 
    for (k,v) in special.items():
        text = text.replace (k, v)

    filtered = filter(lambda x: not re.match(r'^\s*$', x), text) 
    finaltext = re.sub(u'分享：','', filtered)
    return finaltext
#end def

def getmatch(pattern, content):
    match = re.search(pattern, content)
    if(match):
        s = match.start()
        e = match.end()
        #show(content[s:e])
        return content[s:e]
    #endif
    return False
#enddef

def getDate(content):
    if (content==False):
        return ''
    pattern = u'(\d{4}-\d{2}-\d{2}|\d{4}\.\d{2}\.\d{2}|\d{4}年\d{1,2}月\d{1,2}日)'
    date_result = getmatch(pattern, content)

    if (date_result==False):
        return ''

    date_result = re.sub(u'(年|月|日|\-)','.',date_result)
    date_result = getmatch(u'\d{4}.\d{2}.\d{2}', date_result)
    if (date_result==False):
        return ''

    return date_result
#enddef

def getTime(content):
    if (content==False):
        return ''
    pattern = u'\d{1,2}:\d{1,2}'
    time_result = getmatch(pattern, content)
    
    if (time_result==False):
        return ''

    return time_result
#enddef

def getCity(content):
    
    if (content==False):
        return ''
    pattern = u'（.+）'
    city_result = getmatch(pattern, content)
    
    if (city_result==False):
        return ''

    city_result = re.sub(u'(（|）)','', city_result)    
    return city_result
#enddef

class DoubanSpider(CrawlSpider):
    """ General configuration of the Crawl Spider """
    name = 'douban'
    allowed_domains = ["mosh.cn"]
    #allowed_domains = ["www.douban.com"]
    #start_urls = ['http://shanghai.douban.com/events/week-all','http://beijing.douban.com/events/week-all'] # urls from which the spider will start crawling
    start_urls = ['http://www.mosh.cn/beijing/events/latest/', 'http://www.mosh.cn/beijing/events/week/', 'http://www.mosh.cn'] # urls from which the spider will start crawling
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
        
        #get raw title
        title = hxs.xpath('//*[@id="collectinfo"]/text()').extract()[0]
 
        #get raw datetime
        try:
            datetime = hxs.xpath('//div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/p/text()').extract()[0]
        except:
            datetime = hxs.xpath('//div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[2]/text()').extract()[0]

        eventdate = getDate(datetime)        
        eventtime = getTime(datetime)        

        #get raw place
        try:
            place = hxs.xpath('///div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/p[1]/span[2]/text()').extract()[0]
        except:
            place = hxs.xpath('//div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[1]/text()').extract()[0]

        #get raw city
        city = getCity(place)
       
        #get raw category
        category = ''

        #get raw link
        link = response.request.url

        #get raw fee
        fee = '' 

        #get raw feelist
        feelist = ''

        #get raw image
        imageurl = hxs.select('//*[@id="detail_bigimg"]/img/@src').extract()[0]
 
        #get raw desc
        desc = stripHTMLTags(hxs.xpath('//*[@id="introduce"]/div[1]').extract()[0])
        desc = desc.strip()

        #get raw status
        status = '0'

        #get raw md5
        md5 = ''

        #set source
        source = 34
        
        #
        print '[weixiao] title - %s' % title
        print '[weixiao] datetime - %s' % datetime
        print '[weixiao] date - %s' % getDate(datetime)
        print '[weixiao] time - %s' % getTime(datetime)
        print '[weixiao] place - %s' % place
        print '[weixiao] city - %s' % city
        print '[weixiao] imageurl - %s' % imageurl
        print '[weixiao] description - %s' % desc

        #generate the item
        item = WeixiaoItem()
        item['source'] = source
        item['city'] = city
        item['category'] = category
        item['title'] = title
        item['link'] = link
        item['date'] = eventdate
        item['time'] = eventtime
        item['place'] = place
        item['fee'] = fee
        item['feelist'] = feelist
        item['image'] = imageurl
        item['desc'] = desc
        item['status'] = status
        item['md5'] = md5

        yield item
        print "[weixiao] yield ..."

    #end def


