# This Python file uses the following encoding: utf-8
import six
import scrapy
import sys
import hashlib
import re
import time
import md5
from scrapy.selector import Selector
from scrapy.http import Request
from chekucafe.items import WeixiaoItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
def stripAllTags( html ):
	if html is None:
		return ''
	return ''.join( BeautifulSoup( html ).findAll( text = True ) )

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


def getTime(content):
    if (content==False):
        return ''
    pattern = u'\d{1,2}:\d{1,2}'
    time_result = getmatch(pattern, content)

    if (time_result==False):
        return ''

    return time_result
#enddef
 
def getDate(str):
	p=re.compile(u'\d{1,2}月\d{1,2}日')
	str=re.findall(p,str)
	str=re.findall('\d{1,2}',str[0])
	str="2015."+str[0]+"."+str[1]
	return str 
def GetStringMD5(str):  
    m = md5.new()  
    m.update(str)  
    return m.hexdigest()  
def isTargetPage(targetpattern, url):
	regex = re.compile(targetpattern, re.IGNORECASE)
	if(regex.match(url)):
		return True
	return False
def getUrls():
	urls = []
	baseUrl = 'http://www.chekucafe.com/Party/index/page/'
	#urls.append('http://www.chekucafe.com/Party/before')
	for category in range(1,3):
		url1 = baseUrl + str(category)
		urls.append(url1)
	return urls
class ChekucafeSpider(CrawlSpider):
	name = 'chekucafe'
	allowed_domains = ['chekucafe.com']
	start_urls = getUrls()
	rules = ()
	attributes={}
	targetpattern = r'http://www.chekucafe.com/Party/party/id/\d+'
	#Rule(LinkExtractor(allow=('/index/page/\d', )),follow=True,),
	#Rule(LinkExtractor(allow=( ,),)),
	#Rule(LinkExtractor(allow=True), callback='parse_item'),
	#Rule(LinkExtractor(allow=('/party/id/\d{2,3}$', )), callback='parse_item', follow=False,),
	#Rule(LinkExtractor(allow=(, )), callback='parse_item'),
	def __init__(self, name=None, **kwargs):
		super(ChekucafeSpider, self).__init__(name, **kwargs)
		reload(sys)
		self.items_buffer = {}
		sys.setdefaultencoding('utf-8')
		#self.items_buffer = {}
		#from scrapy.conf import settings
		#settings.overrides['DOWNLOAD_TIMEOUT']
		#end def
	def parse(self, response):
		items =response.xpath('/html/body/div/ul/li')
		for index, item in enumerate(items):        
			
			imageurl = item.xpath('.//a/img/@src').extract()
			if(len(imageurl)==0):
				imageurl = ''
			else:
				imageurl = imageurl[0]	
		
			link = 'http://www.chekucafe.com' + item.xpath('.//a/@href').extract()[0]
			print(link)
			title = item.xpath('.//h3/a/text()').extract()[0]
			city=u'北京'
			date=''
			time=''
			#time=item.xpath('/html/body/div/ul/li/div[1]/table/tbody/text()').extract()
			self.attributes[link]=[city,title,imageurl,date,time]
		
			if (isTargetPage(self.targetpattern,link)):
				yield Request( url=link, callback=self.parse_details)
				continue 

	def parse_details(self, response):        
		city = self.attributes[response.url][0]
		title = self.attributes[response.url][1]
		imageurl = self.attributes[response.url][2]
		eventdate = self.attributes[response.url][3]
		eventtime = self.attributes[response.url][4]
		eventtime= response.xpath('/html/body/div/div[1]/article/section/stdong/text()').extract()[0]
		eventdate= response.xpath('/html/body/div/div[1]/article/section/stdong/text()').extract()[0]
		eventdate=getDate(eventdate)
		eventtime=getTime(eventtime)
		place=response.xpath('/html/body/div/aside/address/p/stdong/text()').extract()[0]
                place = place.replace(u'地址：', '')
		fee=response.xpath('/html/body/div/div[@id="party-details"]/article/section/stdong/stdong/stdong/text()').extract()[0]
		feelist=''
		desc = response.xpath('//article[@class="content"]').extract()[0]
		desc = stripAllTags(desc)
		desc = filter(lambda x: not re.match(r'^\s*$', x), desc)
		
		item=WeixiaoItem()
                item['source'] = '19'
		item['md5']=GetStringMD5(response.url)
		item['city']=city
		item['category']='IT-创业'
		#item['detailedCategory']=''
		item['title']=title
		item['link']=response.request.url
		item['date']=eventdate
		item['time']=eventtime
                print eventtime
		item['place']=place
		item['fee']='0'
		item['feelist']=''
		item['image']=imageurl
		item['desc']=desc
		item['status']='0'
		item['created']=time.asctime( time.localtime(time.time()))
		yield item
