
# coding=utf-8
import urllib, urllib2
import sys, os
import re
import time
import string
import threading
import httplib, urlparse
from sets import Set
from PIL import ImageFile
from urlparse import urljoin
from collections import OrderedDict
from BeautifulSoup import BeautifulSoup

def show(message):
    flag = False
    if (flag==True):
        print message
    #endif
#enddef

def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj
#enddef

def to_utf8(obj):
    if isinstance(obj, basestring):
        if isinstance(obj, unicode):
            obj = obj.encode('utf-8')
    return obj
#enddef

def get_encoding(htmlcontent):
    encod = getmatch('charset\s*=\s*\S*"', htmlcontent)
    if encod != False:
        encod = re.sub('(charset\s*=|"|\s)','',encod)
        return encod
    #endif
    encod = getmatch('Charset\s*=\s*\S*"', htmlcontent)
    if encod != False:
        encod = re.sub('(Charset\s*=|"|\s)','',encod)
        return encod
    #endif
    encod = 'utf-8'
    return encod
#enddef

def getHTML(url):
    url = urllib2.urlopen(url)
    htmlcontent = url.read()
    encoding = get_encoding(htmlcontent)
    soup = BeautifulSoup(htmlcontent.decode(encoding,'ignore'))
    return htmlcontent, soup
#end def

def visible(element):
    if element.parent.name in ['style', 'script', 'document', 'head', 'title']: return False
    elif re.match(u'<!--.*-->', str(element)): return False
    elif re.match(u'\n', str(element)): return False
    elif re.match(u'^ *$', str(element)): return False
    else: 
        return True
#enddef

def getPureText(soup):
    texts = soup.findAll(text=True)
    temp_data = filter(visible,texts)
    content = ' '.join(temp_data)
    content = content.replace(u'&#12288;', '')
    content = content.replace(u'&nbsp;', '')
    return content
#enddef

def getDescription(soup):
    description = ''
    error = False
    desc=soup.findAll(attrs={'name':'description'})
    try:
        description = desc[0]['content']
    except:
        error = True
        description = ''
    #endtry    
    if(error==True):
        desc=soup.findAll(attrs={'name':'Description'})
        try:
            description = desc[0]['content']
        except:
            error = True
            description = ''
        #endtry    
    #endif
    return description
#enddef

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

def getTimeSection(content):
    pattern = u'(\d{4}-\d{2}-\d{2}|\d{4}\.\d{2}\.\d{2}|\d{4}年\d{1,2}月\d{1,2}日).*\d{1,2}:\d{1,2}'
    time_result = getmatch(pattern, content)
    return time_result
#enddef

def getDate(content):
    if (content==False):
        return ''
    pattern = u'(\d{4}-\d{2}-\d{2}|\d{4}\.\d{2}\.\d{2}|\d{4}年\d{1,2}月\d{1,2}日)'
    date_result = getmatch(pattern, content)

    if (date_result==False):
        return ''

    date_result = re.sub(u'(年|月|日|\.)','-',date_result)
    date_result = getmatch(u'\d{4}-\d{2}-\d{2}', date_result)
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

def getLocation(content):
    place = u''
    pattern = u'(地\s*点|场\s*馆|场\s*地)(:|：)(\s|\u200b)+([\u4e00-\u9fa5]|[\uff08-\uff09])+'
    place_result = getmatch( pattern, content)
    if(place_result!=False):
        place1 = getmatch(u'(\s|\u200b)+([\u4e00-\u9fa5]|[\uff08-\uff09])+',place_result)
        place1 = re.sub(u'(\uff08|\uff09)','',place1)
        place = getmatch(u'([\u4e00-\u9fa5])+',place1)
        show(place_result)
        show(place1)
        show(place)    
    #endif
    return place
#enddef

def getCity(title, description, content):
    city = u'TBD'
    pattern = u'(北\s*京|上\s*海)'
    city_result = getmatch( pattern, title)
    if(city_result != False):
        return city_result
    #endif
    city_result = getmatch( pattern, description)
    if(city_result != False):
        return city_result
    #endif
    city_result = getmatch( pattern, content)
    if(city_result != False):
        return city_result
    #endif
    return city
#enddef

def getFee(content):
    fee = '0'
    pattern =u'(价\s*位|价\s*格|费\s*用|票\s*价)\s*(:|：)\s*(待\s*定|免\s*费|\D*\d{1,})'
    fee_result = getmatch(pattern, content)
    if(fee_result==False):
        return fee
    #endif
    tmpcontent = re.sub(fee_result,'', content)
    fee_result1 = getmatch(pattern, tmpcontent)
    if(fee_result1!=False):
        if(len(fee_result1)<len(fee_result)):
            fee_result = fee_result1
        #endif
    #endif
    if(fee_result != False):
        fee = getmatch(u'\d{1,}', fee_result)
        if(fee==False):
            return '0'
        #endif
    #endif
    return fee
#enddef

class ImageAnalyzer (threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.size = 0
    #enddef

    def run(self):
        self.size = getImageSize(self.url)
        print self.size, self.url
    #enddef

#end class

def getBiggestImageYet(baseurl, soup, htmlcontent):
    print "starting at %s" % (time.ctime(time.time()))
    imageurls = Set([])
    for tag in soup.findAll('img', src=True):
        image_url = urlparse.urljoin(baseurl, tag['src'])
        image_url = re.sub(u'\.\.','',image_url)
        imageurls.add(image_url)
    #endfor
    #get background-image
    pattern = 'background-image\s*:\s*url\s*(.*);'
    background_images =  re.findall(pattern, htmlcontent)
    for item in background_images:
        try:
            item = re.sub( '[()]', '', item)
            if(item[1]=='/'):
                item_url = 'http:' + item
            else:
                item_url = urlparse.urljoin(baseurl, item_url)
            #endif
            imageurls.add(item_url)
        except:
            continue
        #endtry
    #endfor
    #use multithread to deal with the size problem
    threads = []
    for image_url in imageurls:
        #print image_url
        thread = ImageAnalyzer(image_url)
        thread.start()
        threads.append(thread)
    #endfor
    #wait for all threads to complete
    for t in threads:
        t.join()
    #endfor
    images = {};
    for t in threads:
        images[t.url] = t.size;
        #print t.size, t.url
    #endfor 
    if(len(images)==0):
        return u''
    #sort to get top one, FIXME, we can get top N
    d_sorted_by_value = OrderedDict(sorted(images.items(), key=lambda x: x[1]))
    items = d_sorted_by_value.items()
    items.reverse()
    print "ending at %s" % (time.ctime(time.time()))
    return items[0][0]
#enddef

def getBiggestImage(baseurl, soup, htmlcontent):
    print "starting at %s" % (time.ctime(time.time()))
    images = {};
    for tag in soup.findAll('img', src=True):
        try:
            image_url = urlparse.urljoin(baseurl, tag['src'])
            image_url = re.sub(u'\.\.','',image_url)
            image_size = getImageSize(image_url)
            images[image_url] = image_size
            #print image_url
        except:
            continue
        #endtry
    #endfor
    #get background-image
    pattern = 'background-image\s*:\s*url\s*(.*);'
    background_images =  re.findall(pattern, htmlcontent)
    for item in background_images:
        try:
            item = re.sub( '[()]', '', item)
            if(item[1]=='/'):
                item_url = 'http:' + item
            else:
                item_url = urlparse.urljoin(baseurl, item_url)
            #endif
            item_size = getImageSize(item_url)
            images[item_url] = item_size
        except:
            continue
        #endtry
    #endfor
    if(len(images)==0):
        return ''
    #sort to get top one, FIXME, we can get top N
    d_sorted_by_value = OrderedDict(sorted(images.items(), key=lambda x: x[1]))
    items = d_sorted_by_value.items()
    items.reverse()
    print "ending at %s" % (time.ctime(time.time()))
    return items[0][0]
#enddef

def getBiggestImageAnother(baseurl, soup):
    max_size = 0
    max_url = ''
    for tag in soup.findAll('img', src=True):
        image_url = urlparse.urljoin(baseurl, tag['src'])
        image_size = getImageSize(image_url)
        if(image_size > max_size):
            max_size = image_size
            max_url = image_url
        #endif
    #endfor
    return max_url
#enddef

def getBiggestImageUrl(url):
    soup = getHTML(url)
    return getBiggestImageAnother(url, soup)
#enddef

def getImageSize(uri):
    # get file size *and* image size (None if not known)
    file = urllib.urlopen(uri)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return p.image.size[0] * p.image.size[1]
            break
    file.close()
    return 0
#enddef

def getEvent(url):
    event = {}
    success = 1
    msg = u'ok'
    try:
        try:
            htmlcontent, soup = getHTML(url)
        except:
            url = 'http://' + url
            htmlcontent, soup = getHTML(url)
        #endtry
        event['url'] = to_utf8(url)
        #get title
        title = soup.title.string
        event['title'] = to_utf8(title)
        #get description
        description = getDescription(soup)
        event['description'] = to_utf8(description)
        #get pure text content
        content = getPureText(soup)
        #get time statement
        timesection = getTimeSection(content)
        if (timesection==False):
            timesection = htmlcontent
        #endif
        event['date'] = to_utf8(getDate(timesection))
        if(event['date']==''):
            event['date'] = to_utf8(getDate(content))
        #endif
        event['time'] = to_utf8(getTime(timesection))
        if(event['time']==''):
            event['time'] = to_utf8(getTime(content))
        #endif
        #get city
        event['city'] = to_utf8(getCity(title, description, content))
        #get location
        event['location'] = to_utf8(getLocation(content))
        #get image url
        event['image'] = to_utf8(getBiggestImageYet(url,soup,htmlcontent))
        #get fee information
        event['fee'] = to_utf8(getFee(content))
    except Exception as e:
        success = 0
        msg = str(e)
    #endtry
    
    return success, msg.encode('utf-8'), event  
#enddef

