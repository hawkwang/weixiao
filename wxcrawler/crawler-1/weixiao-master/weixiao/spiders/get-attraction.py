#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
import sys     # 1
import hashlib
from weixiao.items import WeixiaoItem
from weixiao.pipelines import to_unicode_or_bust, validate_time, validate_date

def getPages(number):
    Pages=[]
    for i in range(1,number):
        Pages.append(i)
    #end for
    return Pages
#end def

def getCities():
    City=['beijing', 'shanghai', 'guangzhou']
    return City
#end def

def getCategories():
    Category=['wenyi', 'tiyu', 'qita']
    return Category
#end def

def getDetailedCategories(name):
    DetailedCategory = {}
    DetailedCategory['wenyi'] = ['yanchanghui','huaju','yinlehui','yinleju','xiqu','balewu','qinzijiating','anopera','wuju','theatre','zaji','xiangshengxiaopin','zongyijiemu']
    DetailedCategory['tiyu'] = ['wangqiu','zuqiu','ganlanqiu','sinuoke','gaoerfuqiu','huabing','yumaoqiu','Cbalanqiu','baseball','jinbiaosai','paiqiu','saiche','quanji','youyong','jixianyundong','mashu','tiaoshui']
    DetailedCategory['qita'] = ['dianyingpiao','buobuguantongpiao','zhanlan','huiyi']
    return DetailedCategory[name]
#end def

def getUrls():
    urls = []
    attributes={}
    baseUrl = "http://www.chinaticket.com/"
    for city in getCities():
        url1 = baseUrl + city + '/'
        for category in getCategories():
            url2 = url1 + category + "/"
            detailedCategories = getDetailedCategories(category)
            for detailedCategory in detailedCategories:
                url3 = url2 + detailedCategory 
                for i in range(1,10):
                    url = url3 + '/?o=3&page=' + str(i)
                    urls.append(url)
                    attributes[url] = [city, category, detailedCategory]
                #end for
            #end for
        #end for
    #end for
    return urls, attributes
#end def


class AttractionSpider(CrawlSpider):
	name = "weixiao"
	allowed_domains = ["chinaticket.com"]
	start_urls, attributes = getUrls()
	rules = ()

	def __init__(self, name=None, **kwargs):
		super(AttractionSpider, self).__init__(name, **kwargs)

                reload(sys)
                sys.setdefaultencoding('utf-8') 

		self.items_buffer = {}
		self.base_url = "http://chinaticket.com"
		from scrapy.conf import settings
		settings.overrides['DOWNLOAD_TIMEOUT'] = 360
	#end def
	
	def parse(self, response):
		print "Start scrapping Attractions...."
		try:
			hxs = HtmlXPathSelector(response)
			links = hxs.select('//ul/li[@class="ticket_list_tu fl"]//a/@href')
			if not links:
				return
				log.msg("No Data to scrap")
			#endif
			for link in links:
				v_url = ''.join( link.extract() )
				if not v_url:
					print "[weixiao]- continue..."
					continue
				else:
					_url = v_url
					city = self.attributes[response.url][0]
					category = self.attributes[response.url][1]
					detailedCategory = self.attributes[response.url][2]
					self.attributes[_url] = [city, category, detailedCategory]
					
					print "[weixiao] sending low level url - ", _url
					yield Request( url=_url, callback=self.parse_details )
				#end if
			#end for
		except Exception as e:
			log.msg("Parsing failed for URL {%s}"%format(response.request.url))
			raise
		#end try-except
	#end def

	def parse_details(self, response):
		print "[weixiao] Start scrapping Detailed Info...."
		try:
			hxs = HtmlXPathSelector(response)
			items = []
			city = self.attributes[response.url][0]
			category = self.attributes[response.url][1]
			detailedCategory = self.attributes[response.url][2]
			link = response.request.url.strip()
			title = hxs.xpath('//div[@class="item_big_right"]/h1/text()').extract()[0].strip()
			place = ""
			try:
				place = hxs.xpath('//div[@class="item_big_cg"]/a/text()').extract()[0].strip()
			except Exception as e1:
				place = "unknown"
			#end try-except
			description = hxs.xpath('//div[@class="f_gray_k"]/div[@class="jieshao"]').extract()
			#print "555555555555555555555555555555555555", description
			imageurl = hxs.select('//div[@class="f_k"]/img[@class="itme_big_img"]/@src').extract()[0]
			#print "000000000000000000000000000000000000000000000", imageurl
			#print "image url:", imageurl
			details = hxs.xpath('//ul[@class="f_lb_list"]')
			for detail in details:
				timeitems = detail.xpath('li[@class="f_lb_list_shijian"]/text()')
				i = 0
				eventdate = "unknown"
				eventtime = "unknown"
                                print "---------------------------------------------------------"
                                print timeitems
				for eachitem in timeitems:
                                        current_value = eachitem.extract().strip()
                                        print i
                                        print current_value
					if validate_date(current_value)==True :
						eventdate = current_value
						#print eventdate
					#endif
					if validate_time(current_value)==True :
						eventtime = current_value
						#print eventtime
					#endif
					i+=1
				#endfor 
				fees = detail.xpath('li[@class="f_lb_list_piaojia"]/span/text()')
				feelist = ""
				fee = ""; #minimum price
				i = 0
				for eachfee in fees:
					if i==0:
						fee = eachfee.extract()
						i = 1
					#endif
					feelist += eachfee.extract() + " "
				#end for
				#fee = detail.xpath('li[@class="f_lb_list_piaojia"]/span[1]/text()').extract()[0]
				item = WeixiaoItem()
				item['source'] = 5   # this is hardcoded groupid
				item['city'] = to_unicode_or_bust(city)
				item['category'] = to_unicode_or_bust(detailedCategory)
				item['title'] = to_unicode_or_bust(title)
				item['link'] = link
				item['date'] = eventdate
				item['time'] = eventtime
				item['place'] = to_unicode_or_bust(place)
				item['fee'] = fee
				item['feelist'] = feelist
				item['image'] = imageurl
				item['desc'] = to_unicode_or_bust (title + ' ' + eventdate + ' ' + eventtime + ' ' + place + ' ' + feelist)
				item['status'] = '0'
                                #hash_object = hashlib.md5(city+title+link+eventdate+place)
                                item['md5'] = '' #hash_object.hexdigest()
				items.append(item)
				yield item
				print "[weixiao] yield ..."
				#print eventdate, fee
			#end for
		except Exception as e:
			log.msg("Parsing failed for URL {%s}"%format(response.request.url))
			content = input("we have problem!!!")
			raise
		#end try-except
	#end def 
#end class
