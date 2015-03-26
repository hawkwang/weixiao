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
from tiandaoedu.items import WeixiaoItem
#import redis

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
    pattern = u'(\d{4}-\d{1,2}-\d{1,2}|\d{4}\.\d{1,2}\.\d{1,2}|\d{4}年\d{1,2}月\d{1,2}日)'
    date_result = getmatch(pattern, content)

    if (date_result==False):
        return ''

    date_result = re.sub(u'(年|月|日|\-)','.',date_result)
    date_result = getmatch(u'\d{4}.\d{1,2}.\d{1,2}', date_result)
    if (date_result==False):
        return ''

    return date_result
#enddef

def getAnotherDate(content):
    if (content==False):
        return ''
    pattern = u'(\d{1,2}-\d{1,2}|\d{1,2}\.\d{1,2}|\d{1,2}月\d{1,2}日)'
    date_result = getmatch(pattern, content)

    if (date_result==False):
        return ''

    date_result = re.sub(u'(月|日|\-)','.',date_result)
    date_result = getmatch(u'\d{1,2}.\d{1,2}', date_result)
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
    pattern = u'\].+\|'
    city_result = getmatch(pattern, content)
    
    if (city_result==False):
        return ''

    city_result = re.sub(u'\]','', city_result)    
    city_result = re.sub(u'\|','', city_result)    
    return city_result
#enddef

def getLocation(content):
    place = u''
    pattern = u'地点：\s*(\w|[\u4e00-\u9fa5]|[\u4e00-\u9fa5])+'
    place_result = getmatch( pattern, content)
    if(place_result!=False):
        #place1 = getmatch(u'(\w|[\u4e00-\u9fa5]|[\u4e00-\u9fa5])+',place_result)
        place_result = re.sub(u'地点：\s*','',place_result)
        #place = getmatch(u'([\u4e00-\u9fa5])+',place_result)
    #endif
    return place_result
#enddef

def getUrls():
    urls = []
    baseUrl = 'http://zph.haitou.cc/bj/uni-0/after/hold/page-'
    for category in range(1,10):
        url1 = baseUrl + str(category) + '/'
        urls.append(url1)
    #end for
    #urls.append('http://xjh.haitou.cc/article/208233.html')
    return urls
#end def

class EventSpider(CrawlSpider):
    name = "event"
    allowed_domains = ["http://zph.haitou.cc"]
    start_urls = getUrls()

    attributes={}
    
    rules = ()
    targetpattern = r'http://zph.haitou.cc/article/\d+.html'
    #redisDB = redis.StrictRedis(host='localhost', port=6379, db=0)

    def __init__(self, name=None, **kwargs):
        super(EventSpider, self).__init__(name, **kwargs)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.items_buffer = {}
        from scrapy.conf import settings
        settings.overrides['DOWNLOAD_TIMEOUT'] = 3600
    #end def

    def parse(self, response):
        needitems = []
        try:
            log.msg("Parsing detailed info for URL - %s" % format(response.request.url))
            items = response.xpath('//td[@class="preach-tbody-title"]')
            for index, item in enumerate(items):

                link = item.xpath('.//a/@href').extract()[0]
                link = 'http://zph.haitou.cc' + link
                print link

                if (not link) or (UrlChecker(link)==False):
                    print "Parsing failed for URL {%s}" % format(link)
                    continue
                else:
                    if isTargetPage(self.targetpattern,link):
                        print 'yes ...'
                        f = open('../workfile', 'a')
                        f.write(link+'\n')
                        f.close()
                        #yield Request( link, callback = self.parse_details1 )
                        #if self.redisDB.exists(link)==False :
                        #    self.redisDB.set(link, '0')
                        needitems.append(Request( link, callback = self.parse_details1 ))
                        print 'yes 1 ...'
                        continue    
                    #end if
                #end if

            #end for

        except Exception as e:
            log.msg("Parsing failed for URL {%s}"%format(response.request.url))
            raise
        #end try-except
        print 'return'
        return needitems
    #end def
 
    def parse_details1(self, response):
        print 'hehe'
    #enddef

    def parse_details(self, response):
        print 'yes 2'
        log.msg("Cool -parsing detailed info for URL - %s" % format(response.request.url))
        city = u'北京'
        title = response.xpath('//h3[@class="heading"]').extract()[0]
        title = stripHTMLTags(title)
        imageurl = ''
        print title
        print city

	desc = response.xpath('//div[@class="panel-body-text"]').extract()[0]
        desc = stripHTMLTags(desc)

        eventdate = response.xpath('//div[@class="holdTime"]/text()').extract()
        eventtime = getTime(eventdate)
        eventdate = getDate(eventdate)

        print eventdate
        print eventtime

        place1 = response.xpath('//div[@class="article-info-box"]/div[1]/p[1]/span/text()').extract()[0]
        place2 = response.xpath('//div[@class="article-info-box"]/div[1]/p[3]/span/text()').extract()[0]
        place = place1 + ' ' + place2
        print place

        source = 27
        category = u'招聘-宣讲会'
        link = response.request.url
        #get raw fee, FIXME
        fee = '0' 
        #get raw feelist
        feelist = ''
        #get raw status
        status = '0'
        #get raw md5
        md5 = ''

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

