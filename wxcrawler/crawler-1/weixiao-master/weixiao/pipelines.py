#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from models import Events, db_connect, create_events_table
import hashlib
import time
import pytz
from datetime import tzinfo, timedelta, datetime
import re

def convert_category(category):
    category = re.sub('wangqiu', u'网球', category)
    category = re.sub('zaji', u'杂技', category)
    category = re.sub('huiyi', u'会议', category)
    category = re.sub('saiche', u'赛车', category)
    category = re.sub('yinlehui', u'音乐会', category)
    category = re.sub('huabing', u'滑冰', category)
    category = re.sub('xiangshengxiaopin', u'相声小品', category)
    category = re.sub('yanchanghui', u'演唱会', category)
    category = re.sub('wuju', u'舞剧', category)
    category = re.sub('xiqu', u'戏曲', category)
    category = re.sub('anopera', u'歌剧', category)
    category = re.sub('qinzijiating', u'亲子家庭', category)
    category = re.sub('mashu', u'马术', category)
    category = re.sub('yinleju', u'音乐剧', category)
    category = re.sub('gaoerfuqiu', u'高尔夫球', category)
    category = re.sub('huaju', u'话剧', category)
    category = re.sub('zhanlan', u'展览', category)
    category = re.sub('zuqiu', u'足球', category)
    category = re.sub('theatre', u'电影', category)
    category = re.sub('zongyijiemu', u'综艺节目', category)

    return category
#end def

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
    print 'validate time : ' + t
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

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def makekey(item):
        str_list = []
        str_list.append(item['title'])
        str_list.append(item['link'])
        str_list.append(item['city'])
        str_list.append(item['date'])
        return ''.join(str_list)
    #end def

    def process_item(self, item, spider):
        str_list = []
        str_list.append(item['title'])
        str_list.append(item['link'])
        str_list.append(item['city'])
        str_list.append(item['date'])
        key = ''.join(str_list)
        hash_object = hashlib.md5(key)
        item['md5'] = hash_object.hexdigest()
        # deal with multiple dates 
        dates = item['date'].split('-')
        size = len( dates )
        if size>1 :
            item['date'] = dates[0]
        # if not date format "2015.05.08", drop this item
        isDate = validate_date(dates[0])
        if isDate == False :
            raise DropItem("Do not provide date for this event" % item)
        
        isTime = validate_time(item['time'])
        if isTime == False :
            item['time'] = 'unknown'

        # determine if the event is obsolete one
        year, month, day = get_date_detail(item['date'])
        if isTime == False :
            hour = 0
            minute = 0
        else :
           hour, minute = get_time_detail(item['time'])

        event_time = build_datetime(year, month, day, hour, minute)
        current_china_datetime = datetime.now(pytz.timezone('Asia/Shanghai'))
        if (event_time.isoformat(' ') <= current_china_datetime.isoformat(' ')) :
            raise DropItem("Obsolete item found: %s" % item)

        #item['created'] = time.asctime( time.localtime(time.time()) )
        item['created'] = datetime.utcnow().isoformat(' ')  # replace .now()
        
        if item['md5'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['md5'])
            item['category'] = convert_category(item['category'])
            return item
    #end def
#end class

class LivingSocialPipeline(object):
    """Livingsocial pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_events_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save events in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        event = Events(**item)

        try:
            session.add(event)
            session.commit()
        except:
            session.rollback()
            #raise
            print '[WeixiaoCrawler] - this event already exists ... '
        finally:
            session.close()

        return item
    #end def
#end class

class ComesgPipeline(object):
    def process_item(self, item, spider):
        return item



