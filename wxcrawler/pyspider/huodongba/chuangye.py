#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-04-28 09:45:24
# Project: beijing_ganma

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

attributes={}

class Handler(BaseHandler):
    crawl_config = {
    }
        
    @every(minutes=6 * 60)
    def on_start(self):
        for page in range(1,10):
            self.crawl('http://www.hudongba.mobi/find/p' + str(page) + '-q4a-fu-dbx', callback=self.index_page, force_update=True)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.find_main_li').items():
            #print each
            alink = each('.find_main_title a')
            link = alink.attr.href
            #print alink.text()
            #print link
            #logoarea = each('img.hd_pic')
            #print logoarea
            logo = each('img.hd_pic').attr('data-src')
            print logo
            
            hash_object = hashlib.md5(link)
        
            datearea = each('.find_main_time p')
            #print datearea.text()
            date = getDate(datearea.text())
            time = '00:00'
            #print date
            address =  each('.find_main_address a').text()
            #print address
            
            title = alink.text()
            desc = alink.text()
        
            # if not date format "2015.05.08", drop this item
            isDate = validate_date(date)
            if isDate == False :
                return

            isTime = validate_time(time)
            if isTime == False :
                return

            # determine if the event is obsolete one
            year, month, day = get_date_detail(date)
            if isTime == False :
                hour = 0
                minute = 0
            else :
               hour, minute = get_time_detail(time)

            event_time = build_datetime(year, month, day, hour, minute)
            current_china_datetime = datetime.now(pytz.timezone('Asia/Shanghai'))
            if (event_time.isoformat(' ') <= current_china_datetime.isoformat(' ')) :
                print "Obsolete item found ..."
                return
                #raise DropItem("Obsolete item found: %s" % item)

            created = datetime.utcnow().isoformat(' ')  # replace .now()
            fee = '0'
            
            result = {
                "md5": hash_object.hexdigest(),
                "source": '37',
                "city": 'beijing',
                "category": u'创业',
                "title": title,
                "link": link,
                "date": date,
                "time": time,
                "place": address,
                "fee": fee,
                "feelist": '',
                "image": logo,
                "desc": desc,
                "status": '0',
                "created": created,
            }
        
            #print result
    
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

