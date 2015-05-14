
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-05-14 13:03:04
# Project: huodongjia_it

from pyspider.libs.base_handler import *
import urllib
import urllib2
#from urllib2 import *
import json
import traceback
import re
import hashlib
import pytz
from datetime import tzinfo, timedelta, datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import time

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'lelespider',
            'password': '1111111',
            'database': 'lelespider'}

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**DATABASE))


def create_events_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

class Events(DeclarativeBase):
    """Sqlalchemy events model"""
    __tablename__ = "events"

    md5 = Column('md5', String, primary_key=True)
    title = Column('title', String)
    desc = Column('desc', String, nullable=True)
    link = Column('link', String, nullable=True)
    areacode = Column('areacode', String, nullable=True)
    category = Column('category', String, nullable=True)
    fee = Column('fee', String, nullable=True)
    feelist = Column('feelist', String, nullable=True)
    source = Column('source', String, nullable=True)
    city = Column('city', String, nullable=True)
    place = Column('place', String, nullable=True)
    date = Column('date', String, nullable=True)
    time = Column('time', String, nullable=True)
    image = Column('image', String, nullable=True)
    status = Column('status', String, nullable=True)
    created = Column('created', String, nullable=False)
#end class


def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

def validate_date(d):
    try:
        datetime.strptime(d, '%Y.%m.%d')
        return True
    except ValueError:
        return False
#end def

def validate_time(t):
    #print 'validate time : ' + t
    try:
        datetime.strptime(t, '%H:%M')
        return True
    except ValueError:
        return False
#end def

def isTargetPage(targetpattern, url):
    regex = re.compile(targetpattern, re.IGNORECASE)
    if(regex.match(url)):
        return True
    return False
#end def

def get_date_detail(d):
    try:
        date = datetime.strptime(d, '%Y.%m.%d')
        return date.year, date.month, date.day
    except ValueError:
        return False
#end def

def get_time_detail(t):
    try:
        date = datetime.strptime(t, '%H:%M')
        return date.hour, date.minute
    except ValueError:
        return False
#end def

def build_datetime(year, month, day, hour, minute, tz=pytz.timezone('Asia/Shanghai')):
    ctt = datetime(year, month, day, hour, minute, 0, 0, tz)
    return ctt
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

def getHappenDate(content, year='2015'):
    if (content==False):
        return ''
    pattern = u'(\d{1,2}月\d{1,2}日)'
    date_result = getmatch(pattern, content)

    if (date_result==False):
        return ''

    date_result = re.sub(u'(年|月|日|\-)','.',date_result)
    date_result = getmatch(u'\d{1,2}.\d{1,2}', date_result)
    if (date_result==False):
        return ''

    return year + "." + date_result
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

def getTime(content):
    if (content==False):
        return ''
    pattern = u'\d{1,2}:\d{1,2}'
    time_result = getmatch(pattern, content)

    if (time_result==False):
        return ''

    return time_result
#enddef


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=12 * 60)
    def on_start(self):
        pages = {1,2,3,4,5}
        for page in pages:
            try:
                time.sleep(5)
                url = 'http://m.huodongjia.com/list_ajax/beijing/medical/?page=' + str(page)
                response = urllib2.urlopen(url, None).read()
                #print response
                json_data = json.loads(response)
                #print json_data['messageType']
                for each in json_data['list']:
                    #print each
                    link = 'http://m.huodongjia.com' + each['event_url']
                    hash_object = hashlib.md5(link)
                    md5 = hash_object.hexdigest()
                    source = '35'
                    city = 'beijing'
                    category = u'医疗'
                    image = each['event_img']
                    #place = each['event_venue']
                    place = each['event_address']
                    place = place.replace('\n', ' ')
                    place = place.strip()
                    print place
                    print each['event_address']
                    eventdate = getDate(each['event_begin_time'])
                    eventtime = '00:00'
                    #print eventdate
                    desc = each['content']
                    #print each['head']
                    title = each['head']['title']
                    titles = re.split('-|_',title)
                    title = titles[0]
                    print title
                    print each['head']['title']
                    #keywords = each['head']['keywords']
                    #keywords = keywords.split(',')
                    #title = keywords[0]
                    #print title
                    tmpcategory = category
                    for eachtag in each['event_tag']:
                        if eachtag == tmpcategory:
                            continue
                        category = category + '-' + eachtag
                    print category
                    status = '0'
                    created = datetime.utcnow().isoformat(' ')  # replace .now()
                    fee = '0'
                
                    result = {
                        "md5": md5,
                        "source": source,
                        "city": 'beijing',
                        "category": category,
                        "title": title,
                        "link": link,
                        "date": eventdate,
                        "time": eventtime,
                        "place": place,
                        "fee": fee,
                        "feelist": '',
                        "image": image,
                        "desc": desc,
                        "status": '0',
                        "created": created,
                    }
                
                    print result
                
                    #self.saveResult(result)
                
            except Exception, e:
                traceback.print_exc()
            
        #self.crawl('http://m.huodongjia.com/list_ajax/beijing/medical/?page=1&_=1431579513747', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        #print response.doc().text()
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    def saveResult(self, result):
        print result
        
        if not result or not result['title']:
            return
        eventdate = result['date']
         
        # determine if the event is obsolete one
        year, month, day = get_date_detail(eventdate)
        isTime = False
        if  isTime == False :
               hour = 0
               minute = 0
        else :
           hour, minute = get_time_detail(time)

        event_time = build_datetime(year, month, day, hour, minute)
        current_china_datetime = datetime.now(pytz.timezone('Asia/Shanghai'))
        if (event_time.isoformat(' ') <= current_china_datetime.isoformat(' ')) :
            print "Obsolete item found ..."
            return
            
        print "save this item"
            
        engine = db_connect()
        create_events_table(engine)
        self.Session = sessionmaker(bind=engine)
         
        session = self.Session()
        event = Events(**result)
 
        try:
            session.add(event)
            session.commit()
        except:
            session.rollback()
            #raise
            print '[WeixiaoCrawler] - this event already exists ... '
        finally:
            session.close()
            
    #end def
    
    
