#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-06-29 09:41:20
# Project: nlc

from pyspider.libs.base_handler import *
import re
import hashlib
import pytz
from datetime import tzinfo, timedelta, datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

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


def tsplit(string, delimiters):
    """Behaves str.split but supports multiple delimiters."""

    delimiters = tuple(delimiters)
    stack = [string,]

    for delimiter in delimiters:
        for i, substring in enumerate(stack):
            substack = substring.split(delimiter)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i+j, _substring)

    return stack

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=12 * 60)
    def on_start(self):
        #for page in range(1,10):
        self.crawl('http://wap.nlc.gov.cn/movienotices/index?vt=2&page='+str(1), callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
            
        for each in response.doc('div.result p').items():
            content = each.text()
            print content
            anotherall = tsplit(content, (u'序号:', u'栏目:', u'题目:', u'主讲人:', u'时间:', u'地点:'))
            for eachitem in anotherall :
                print eachitem
                
            date = getHappenDate(content,'2015')
            time = getTime(content)
            #print date
            #print time
            
            #address = each('address').text()
            
            #attributes[detailpage] = [date, time, address]
            #print attributes
            link = response.url
            hash_object = hashlib.md5( link + anotherall[1] )
            
            # if not date format "2015.05.08", drop this item
            isDate = validate_date(date)
            if isDate == False :
                return

            isTime = validate_time(time)
            if isTime == False :
                return

            # determine if the event is obsolete one
            year, month, day = get_date_detail(date)
            if  isTime == False :
                hour = 0
                minute = 0
            else :
               hour, minute = get_time_detail(time)

            event_time = build_datetime(year, month, day, hour, minute)
            current_china_datetime = datetime.now(pytz.timezone('Asia/Shanghai'))
            if (event_time.isoformat(' ') <= current_china_datetime.isoformat(' ')) :
                print "Obsolete item found ..."
                continue

            created = datetime.utcnow().isoformat(' ')  # replace .now()
            
            fee = '0'
            
            result = {
                "md5": hash_object.hexdigest(),
                "source": '36',
                "city": 'beijing',
                "category": u'讲座',
                "title": anotherall[3],
                "link": response.url,
                "date": date,
                "time": time,
                "place":  u"中国国家图书馆",
                "fee": fee,
                "feelist": '',
                "image": "",
                "desc": content,
                "status": '0',
                "created": created,
            }
            
            yield result

    def on_result(self, result):
        
        if not result or not result['title']:
            return
        
        print result
        
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
            

