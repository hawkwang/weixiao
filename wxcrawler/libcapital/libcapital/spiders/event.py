#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
import sys     # 1
import hashlib
import re
from libcapital.items import WeixiaoItem

#from weixiao.items import WeixiaoItem
#from weixiao.pipelines import to_unicode_or_bust, validate_time, validate_date

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
    pattern = u'(\d{4}-\d{2}-\d{2}|\d{4}\.\d{2}\.\d{2}|\d{4}/\d{2}/\d{2}|\d{4}年\d{1,2}月\d{1,2}日)'
    date_result = getmatch(pattern, content)

    if (date_result==False):
        return ''

    date_result = re.sub(u'(年|月|日|\-|/)','.',date_result)
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
            source = '42'
            city = 'beijing'
            category = ''
            link = response.request.url

            #get raw fee, FIXME
            fee = '0' 

            #get raw feelist
            feelist = ''
            
            datetime = hxs.select('//*[@id="events_info"]/div[3]/text()').extract()[0].strip()
            eventdate = getDate(datetime) 
            eventtime = getTime(datetime) 

            place = hxs.select('//*[@id="events_info"]/div[4]/text()').extract()[0].strip()
            place = re.sub(u'首图',u'首都图书馆',place)

            desc = stripHTMLTags(hxs.select('//*[@id="events_related_info"]').extract()[0])
            desc = re.sub(u'预告', u'预告 - ', desc.strip())
            
            imageurl = hxs.select('//*[@id="example1"]/@href').extract()[0]

            status = '0'
            md5 = ''
            
            #
            log.msg( '[weixiao] title - %s' % title, level=log.INFO)
            log.msg( '[weixiao] date - %s' % eventdate, level=log.INFO)
            log.msg( '[weixiao] time - %s' % eventtime, level=log.INFO)
            log.msg( '[weixiao] place - %s' % place, level=log.INFO)
            log.msg( '[weixiao] city - %s' % city, level=log.INFO)
            log.msg( '[weixiao] link - %s' % link, level=log.INFO)
            log.msg( '[weixiao] imageurl - %s' % imageurl, level=log.INFO)
            log.msg( '[weixiao] description - %s' % desc, level=log.INFO)

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

        except Exception as e:
            raise
        #end try-except
    #end def

#end class
