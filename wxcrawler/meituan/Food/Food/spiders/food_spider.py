# -*- coding: utf-8 -*- 
import scrapy
from Food.items import WeixiaoItem
from scrapy.http import Request
from scrapy.selector import Selector
import re
import sys

def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj
#end def

class food_spider(scrapy.Spider):
	
        reload(sys)
        sys.setdefaultencoding('utf-8')
 	name = "food.org"
	start_urls = [
	"http://bj.meituan.com/category/meishi/all/"
	#"http://bj.meituan.com/category/meishi/all/page1"
	]
	#start_urls = ["http://bj.meituan.com/deal/27597943.html"]

	#def parse(self, response):
	#	#items=[]
	#	item = FoodItem()
	#	item['link'] = response.xpath('//a[@class="deal-tile__cover"]/@href').extract()
	#	yield item
	def parse(self, response):
		items = []
		urls = []
		for i in range(1,10):
		#i = 1
			urls.append(response.url + "page" + str(i)) 
			items.extend([Request(url, callback = self.parse_page) for url in urls])
		return items

	def parse_page(self, response):

		sites = response.xpath('//a[@class="deal-tile__cover"]')
		items = []
		for site in sites:
			link = site.xpath('@href').extract().pop()
			#items.append(link)
			info = Request(link, callback = self.parse_url)
			items.append(info)
		return items
		
	def parse_url(self, response): 
		sel = Selector(response)
		
		title_prefix = response.xpath('//span[@class="deal-component-title-prefix"]/text()').extract()[0]
		title = response.xpath('//h1[@class="deal-component-title"]/text()').extract()[0]
		title = title_prefix + title

		fee = response.xpath('//div[@class="deal-component-price cf"]/h2/strong/text()').extract()[0]
		
		link = response.url
		
		image = response.xpath('//img[@class="focus-view"]/@src').extract()[0]

		time = "00:00"
		time = time
		
		dates = sel.xpath('//div[@class="deal-term"]/dl/dd/text()').extract()[0]#.re('\d{4}\.\d{1,2}\.\d{1,2}')
		date = re.findall(r'\d{4}\.\d{1,2}\.\d{1,2}', dates).pop()

		desc1 = response.xpath('//div[@class="deal-component-description"]/text()').extract()
		desc2 = response.xpath('//div[@id="anchor-bizinfo"]/div/p/text()').extract()
		if desc2:
			desc = desc1[0] + desc2[0]
		else:
			desc = desc1[0]

		places = response.xpath('//div[@class="all-biz cf"]/@data-poi').extract()[0].encode('utf-8')
		place = re.findall(r'address.*?,', places)# ['address":"\uxxxx\uxxxx...\uxxxx",', 'address":"...",', ...]
                locations = []		
		if len(place) > 2:
			place = place[0:3]
                        locations.append(place[0][10:-2])
                        locations.append(place[1][10:-2])
                        locations.append(place[2][10:-2])
			place = place[0][10:-2] + "||" + place[1][10:-2] + "||" + place[2][10:-2]
		elif len(place) == 2:
                        locations.append(place[0][10:-2])
                        locations.append(place[1][10:-2])
			place = place[0][10:-2] + "||" + place[1][10:-2]
		else:
                        locations.append(place[0][10:-2])
			place = place[0][10:-2]

		j = 0
		places = ''
		while j < len(place):
			if place[j] == '\\':
				places = places + unichr(int(place[j + 2:j + 6],16))
				j = j + 6
			else:
				places = places + place[j]
				j = j + 1 

		place = places
                print to_unicode_or_bust(place)
                locations = place.split('||')
                
                for location in locations :
		    item = WeixiaoItem()
                    item['category'] = u'美食'
                    item['source'] = '28'
                    item['city'] = 'beijing'
                    item['feelist'] = ''
                    item['md5'] = ''
                    item['status'] = '0'
                    item['place'] = location
                    item['title'] = title
                    item['desc'] = desc + u'有效期至：' + date
                    item['link'] = link
                    item['image'] = image
                    item['date'] = date
                    item['time'] = time
                    item['fee'] = fee
                    item['feelist'] = ''

                    print to_unicode_or_bust(item['title'])
                    print to_unicode_or_bust(item['place'])

                    yield item
                #endfor

