#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urlparse
#from pybloomfilter import BloomFilter
import time
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
from BeautifulSoup import BeautifulSoup

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

def stripAllTags( html ):
    if html is None:
        return ''
    return ''.join( BeautifulSoup( html ).findAll( text = True ) )

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
    content = content.replace('/','.')
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
    content = content.replace('/','.')
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

def getDetailedTime(content):
    if (content==False):
        return ''
    pattern = u'\d{1,2}:\d{1,2} (AM|PM)'
    time_result = getmatch(pattern, content)

    if (time_result==False):
        return '00:00'
    #endif

    #get time without am or pm
    pattern = u'\d{1,2}:\d{1,2}'
    time_without_am_or_pm = getmatch(pattern, time_result) 

    #get am or pm
    pattern = u'AM|PM'
    isafternoon = getmatch(pattern, time_result)
    if(isafternoon=='AM'):
        return time_without_am_or_pm

    #deal with pm time
    timedetail = time_without_am_or_pm.split(':')
    hour = int(timedetail[0]) + 12
    mini = int(timedetail[1])
    
    return str(hour) + ':' + timedetail[1]
    
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
    baseUrl = 'http://bj.huodongxing.com/eventlist?orderby=n&city=北京&page='
    for category in range(1,50):
        url1 = baseUrl + str(category)
        urls.append(url1)
    #end for

#    baseUrl = 'http://bj.huodongxing.com/eventlist?orderby=v&city=北京&page='
#    for category in range(1,10):
#        url1 = baseUrl + str(category)
#        urls.append(url1)
#    #end for

#    baseUrl = 'http://bj.huodongxing.com/eventlist?orderby=r&city=北京&page='
#    for category in range(1,10):
#        url1 = baseUrl + str(category)
#        urls.append(url1)
#    #end for

    return urls
#end def


class EventSpider(CrawlSpider):
    name = "event"
    allowed_domains = ["huodongxing.com"]
    start_urls = getUrls()

    attributes={}
    
    rules = ()
    targetpattern = r'http://www.huodongxing.com/event/\d+.'
    #bf = BloomFilter(10000000, 0.001, 'filter.bloom')

    def __init__(self, name=None, **kwargs):
        super(EventSpider, self).__init__(name, **kwargs)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.items_buffer = {}
        from scrapy.conf import settings
        settings.overrides['DOWNLOAD_TIMEOUT'] = 3600
    #end def

    def parse(self, response):
        try:
            log.msg("Parsing detailed info for URL - %s" % format(response.request.url))
            #time.sleep(5)
            items = response.xpath('//ul[@class="event-horizontal-list-new"]/li')
            for index, item in enumerate(items):
                #print item.extract()
                imageurl = item.xpath('.//a/img/@src').extract()
	        if(len(imageurl)==0):
	            imageurl = ''
	        else:
	            imageurl = imageurl[0]

                link = 'http://www.huodongxing.com' + item.xpath('.//h3/a/@href').extract()[0]
                #print link

                title = item.xpath('.//h3/a/text()').extract()[0]

                city = u'北京'

                #datetime = item.xpath('.//span[@class="time"]/text()').extract()[0]
                firstItem = item.xpath('.//div').extract()[0]
                datetime = stripHTMLTags(firstItem)
                #print datetime
                date = getAnotherDate(datetime)
                #time = getTime(datetime)
                time = '00:00'
                month = int(date.split(".")[0])
                year = '2015'
                #if(month<6):
                #    year = '2015'
                date = year + '.' + date
                #print date
                #print time

                #print title
                #print city

                self.attributes[link] = [city, title, imageurl, date, time]

                if (not city) or (not link) or (UrlChecker(link)==False):
                    print "Parsing failed for URL {%s}" % format(link)
                    continue
                else:
                    print link
                    if (isTargetPage(self.targetpattern,link)):
                        #self.bf.add(link)
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
        time.sleep(5)
        #time.sleep(5)
        city = self.attributes[response.url][0]
        title = self.attributes[response.url][1]
        imageurl = self.attributes[response.url][2]
        eventdate = self.attributes[response.url][3]
        eventtime = self.attributes[response.url][4]

        timedetailinfo = response.xpath('//div[@class="media-body"]/div[1]').extract()[0]
        timedetailinfo = getDetailedTime(timedetailinfo)
        print timedetailinfo

        print title
        #print city

	desc = response.xpath('//div[@id="event_desc_page"]').extract()[0]
        #desc = stripHTMLTags(desc)
        desc = stripAllTags(desc)
        desc = filter(lambda x: not re.match(r'^\s*$', x), desc)
        print desc

        place = response.xpath('//div[@class="address"]/a/text()').extract()[0]
        #print place

        source = 17

        try:
            category = response.xpath('//div[@class="tags"]/a/text()').extract()[0]
        except Exception as e:
            category = ''

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
        item['time'] = timedetailinfo
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

