#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urlparse

import scrapy
from scrapy import log
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import sys
import re
import random
from csdn.items import WeixiaoItem

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
        pattern = u'\d{1,2}时\d{1,2}'
        time_result = getmatch(pattern, content)
        if (time_result==False):
            return ''
        else:
            time_result = time_result.replace(u'时',':')
        #endif
    #endif

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


class HuiyiSpider(CrawlSpider):
    name = "huiyi"
    allowed_domains = ["csdn.net"]
    start_urls = [
        'http://huiyi.csdn.net/activity/home?&page=1', 
        'http://huiyi.csdn.net/activity/home?&page=2', 
        'http://huiyi.csdn.net/activity/home?&page=3', 
        'http://huiyi.csdn.net/activity/home?&page=4', 
        'http://huiyi.csdn.net/activity/home?&page=5', 
        'http://huiyi.csdn.net/activity/home?&page=6', 
        'http://huiyi.csdn.net/activity/home?&page=7', 
        'http://huiyi.csdn.net/activity/home?&page=8', 
        'http://huiyi.csdn.net/activity/home?&page=9', 
        'http://huiyi.csdn.net/activity/home?&page=10']

    attributes={}
    
    rules = ()
    targetpattern = r'http://huiyi.csdn.net/activity/product/goods_list\?project_id=\d+'

    def __init__(self, name=None, **kwargs):
        super(HuiyiSpider, self).__init__(name, **kwargs)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.items_buffer = {}
        from scrapy.conf import settings
        settings.overrides['DOWNLOAD_TIMEOUT'] = 3600
    #end def

    def parse(self, response):
        try:
            log.msg("Parsing detailed info for URL - %s" % format(response.request.url))
            #hxs = HtmlXPathSelector(response)
            #items = hxs.select('//div[@class="item clearfix"]')
            items = response.xpath('//div[@class="item clearfix"]')
            for index, item in enumerate(items):
                #print item.extract()
                date = item.xpath('.//div[@class="month"]/text()').extract()[0]
                city = item.xpath('.//div[@class="addr"]/text()').extract()[0]
                link = item.xpath('.//div[@class="dis"]/dl/dt/a/@href').extract()[0]
                title = item.xpath('.//div[@class="dis"]/dl/dt/a/text()').extract()[0]
                place = item.xpath('.//div[@class="dis"]//dd/a/text()').extract()[0]
                #print title
                #print link
                self.attributes[link] = [city, title, place]

                if (not link) or (UrlChecker(link)==False):
                    print "Parsing failed for URL {%s}" % format(link)
                    continue
                else:
                    if isTargetPage(self.targetpattern,link):
                        yield Request( url=link, callback=self.parse_details)
                        continue    
                    #end if
                #end if

            #end for

        except Exception as e:
            log.msg("Parsing failed for URL {%s}"%format(response.request.url))
            raise
        #end try-except

    #end def

    def parse_details(self, response):
        log.msg("Cool -parsing detailed info for URL - %s" % format(response.request.url))

        title = self.attributes[response.url][1]
        city = self.attributes[response.url][0]
        place = self.attributes[response.url][2]

        datetime = response.xpath('//div[@class="act-head"]//dd/text()').extract()[0]
        print datetime
        eventdate = getDate(datetime)  
        print eventdate
        datetime = response.xpath('//div[@class="addr-time"]//li[1]/text()').extract()[0]
        print datetime
        eventtime = getTime(datetime)
        print eventtime

        #get raw image
        imageurl = response.xpath('//img[@class="ads"]/@src').extract()
        if(len(imageurl)==0):
            imageurl = ''
        else:
            imageurl = imageurl[0]
 
        #get raw desc
        desc = stripHTMLTags(response.xpath('//div[@class="intro dec"]').extract()[0])
        desc = desc.strip()
        #print desc

        category = ''

        #get raw link
        link = response.request.url

        #get raw fee, FIXME
        fee = '0' 

        #get raw feelist
        feelist = ''

        #get raw status
        status = '0'

        #get raw md5
        md5 = ''

        #set source
        source = 44 #FIXME
        
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

        #print item
        yield item
        print "[weixiao] yield ..."
                

    #end def



