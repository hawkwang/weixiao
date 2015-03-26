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
from BeautifulSoup import BeautifulSoup

def getUniversityDict():
    dict = {}
    dict[u'清华大学'] = 'http://bcscdn.baidu.com/resource/fFhOZUjbBmkRuWAwlpP_XWRLlp0_NFVOZUZMuUgYBUgbZj.jpg' 
    dict[u'北京大学'] = 'http://www.microfotos.com/pic/0/39/3910/391007preview4.jpg'
    dict[u'中国人民大学'] = 'http://rucweb-wordpress.stor.sinaapp.com/uploads/2013/09/shi1.jpg' 
    dict[u'北京理工大学'] = 'http://www.bit.edu.cn/images/2013zzgb/logo.jpg' 
    dict[u'北京航空航天大学'] = 'http://bcscdn.baidu.com/resource/fFhOZUjbBmkRBWZwlpP_XWRLlp0_NFVOZUZMuUgYBUZYBL.jpg'
    dict[u'北京科技大学'] = 'http://a4.att.hudong.com/56/68/01300000633474126265686676483.jpg'
    dict[u'北京邮电大学'] = 'http://edu.21cn.com/news/upload/image/20140514/2014051414110879879.PNG'
    dict[u'北京交通大学'] = 'http://gkcx.eol.cn/upload/adminup/2006-09-07/14_21_35_40.jpg'
    dict[u'北京师范大学'] = 'http://www.xx100e.com/Article/UploadFiles/201310/2013101307210429.jpg'
    dict[u'中央财经大学'] = 'http://bcscdn.baidu.com/resource/fFhOZUjbBIjwZmhYlpP_XWRLlp0_NFVOZUZMuUgYBUAqZj.jpg'
    dict[u'中国政法大学'] = 'http://pic.baike.soso.com/p/20131115/20131115141736-1593990689.jpg'
    dict[u'对外经济贸易大学'] = 'http://gkcx.eol.cn/upload/201405091212392688416179053.jpg'
    dict[u'中国矿业大学(北京)'] = 'http://www.cumtb.edu.cn/frameset/2.jpg'
    dict[u'华北电力大学'] = 'http://gkcx.eol.cn/upload/201405091217153525086520659.jpg'
    dict[u'中国农业大学'] = 'http://g.hiphotos.baidu.com/baike/c0%3Dbaike116%2C5%2C5%2C116%2C38/sign=325a8cfd32fa828bc52e95b19c762a51/c9fcc3cec3fdfc031c21eb40d53f8794a5c226e8.jpg'
    dict[u'中国石油大学(北京)'] = 'http://g.hiphotos.baidu.com/baike/c0%3Dbaike80%2C5%2C5%2C80%2C26/sign=c9a9f3ac271f95cab2f89ae4a87e145b/1c950a7b02087bf45472a13bf0d3572c10dfcf42.jpg'
    dict[u'北京化工大学'] = 'http://g.hiphotos.baidu.com/baike/ew%3D86/sign=35f2fe519045d688b148baac92c37dab/f636afc379310a554516e996b54543a9822610a5.jpg'
    dict[u'北京工业大学'] = 'http://h.hiphotos.baidu.com/baike/c0%3Dbaike150%2C5%2C5%2C150%2C50/sign=02abeb39ad51f3ded7bfb136f5879b7a/4034970a304e251f0a77c70ba586c9177e3e5344.jpg'
    dict[u'中国地质大学(北京)'] = 'http://p6.qhimg.com/t014443f281399d54d7.jpg'
    dict[u'中央民族大学'] = 'http://gaokao.zgjhjy.com/UpFiles/%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%A1%A3%286%29.jpg'
    dict[u'中国传媒大学'] = 'http://www.2ok.com.cn/productpic/wsbyzc/info_20138515385746827.jpg'
    dict[u'北京外国语大学'] = 'http://pic.baike.soso.com/p/20131114/20131114154258-1965355399.jpg'

    return dict
#enddef

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
        return '00:00'
    pattern = u'\d{1,2}:\d{1,2}'
    time_result = getmatch(pattern, content)
    
    if (time_result==False):
        pattern = u'\d{1,2}时\d{1,2}'
        time_result = getmatch(pattern, content)
        if (time_result==False):
            return '00:00'
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
    f = open('../workfile', 'r')
    for line in f:
        url = line.replace ( "\n", "" )
        print url
        urls.append(url)
    f.close()
    return urls
#end def

class EventSpider(CrawlSpider):
    name = "event"
    allowed_domains = ["http://zph.haitou.cc"]
    start_urls = getUrls()

    attributes={}
    
    rules = ()
    universities = getUniversityDict()

    def __init__(self, name=None, **kwargs):
        super(EventSpider, self).__init__(name, **kwargs)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.items_buffer = {}
        from scrapy.conf import settings
        settings.overrides['DOWNLOAD_TIMEOUT'] = 3600
    #end def

    def parse(self, response):
        log.msg("Cool -parsing detailed info for URL - %s" % format(response.request.url))
        city = u'北京'
        datetimenode = response.xpath('//span[@id="holdTime"]')
        #print datetimenode
        place1 = datetimenode.xpath('../../p[1]/span/text()').extract()[0]
        place2 = datetimenode.xpath('../../p[3]/span/text()').extract()[0]
        place = place1 + ' ' + place2
        print place

        title = response.xpath('//h3/text()').extract()[1]
        
        print 'title - ' + title
        #title = stripHTMLTags(title)
        imageurl = ''
        print title
        print city

        descnodes = response.xpath('//div[@id="kz-web"]/div[2]/div[1]/div[1]/div[3]/node()').extract()
        desc = ''
        for index, node in enumerate(descnodes):
            #print stripAllTags(node)
            desc = desc + stripAllTags(node).strip()
        #endfor
        desc = filter(lambda x: not re.match(r'^\s*$', x), desc)
        print desc
	#desc = response.xpath('//div[@class="panel-body-text"]/text()').extract()
        #desc = stripHTMLTags(desc)
        #print desc
        eventdate = response.xpath('//span[@id="holdTime"]/text()').extract()[0]
        eventtime = getTime(eventdate)
        eventdate = getDate(eventdate)

        print eventdate
        print eventtime

        source = 27
        category = u'招聘-招聘会'
        link = response.request.url
        #get raw fee, FIXME
        fee = '0' 
        #get raw feelist
        feelist = ''
        #get raw status
        status = '0'
        #get raw md5
        md5 = ''
        
        if place1 in self.universities.keys():
            imageurl = self.universities[place1]

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

