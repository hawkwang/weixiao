#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from urllib2 import *
from sqlalchemy.orm import sessionmaker, relationship
from models import db_connect, create_events_table
from models import Events, Faddress, Address, SimTask
import hashlib
import time
import pytz
from datetime import tzinfo, timedelta, datetime
from solr import Solr
import sys
#from map.googlemap import getDetailedInfo
#from map.baidumap import getDetailedInfo
from address import getDetailedInfo
import json

def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj
#end def

def is_num(value):
    try:
        i = float(value)
    except ValueError, TypeError:
        return False
    #endtry
    return True
#enddef

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

def get_current_time_str():
    current_china_datetime = datetime.now(pytz.timezone('Asia/Shanghai'))
    return current_china_datetime.isoformat(' ')
#end def

def mysleep(count):
    if(count!=0):
        if(count>6):
            count = 6
        print '[WeixiaoSim : ' + get_current_time_str()  + '] - sleep ' + str(count*10) + ' seconds...'
        time.sleep(count*10)
#enddef

class WeixiaoSim(object):
    def __init__(self, url): #url is the lele service API url
        self.url = url
        engine = db_connect()
        create_events_table(engine)
        self.Session = sessionmaker(bind=engine)
    #end def

    # the duplicate_removal flag is used to indicate if duplicate removal feature is used
    def process(self, duplicate_removal=False):
        print 'processing...' 
        session = self.Session()
        flag = True
        sleepcount = 0
        while flag==True:
            flag = True

            # sleep sleepcount interval time
            mysleep( sleepcount )

            if(sleepcount==0):
                sleepcount = 1
            else:
                sleepcount = sleepcount + 1
            #endif

            print '[WeixiaoSim : ' + get_current_time_str()  + '] - new loop to see if we have newly found events...' 
            for instance in session.query(Events).filter(Events.status=='0').filter(Events.city=='beijing').order_by(Events.date, Events.time).limit(10000):
                #flag = True
                sleepcount = 0
                print 'Processing event - ' + instance.title.encode('utf-8') + ' ' + instance.place.encode('utf-8')
                source = instance.source
                title = instance.title
                desc = instance.desc
                date = instance.date
                time = instance.time
                place = instance.place
                fee = instance.fee
                feelist = instance.feelist
                imageurl = instance.image
                print place.encode('utf-8')
                print date
                print time

                if is_num(fee) == False :
                    instance.status = '2'
                    print 'Note: fee (' + fee + ') is strange. So we will skip it...'
                    session.commit()
                    continue
                #endif

                # determine if the event is obsolete one
                year, month, day = get_date_detail(date)
                if validate_time(time) == False :
                    instance.status = '2'
                    print 'Note: time (' + time + ') is strange. So we will skip it...'
                    session.commit()
                    continue
                else :
                    hour, minute = get_time_detail(time)
                
                event_time = build_datetime(year, month, day, hour, minute)
                current_china_datetime = datetime.now(pytz.timezone('Asia/Shanghai'))
                if (event_time.isoformat(' ') <= current_china_datetime.isoformat(' ')) :
                    print 'Note: ' + title + ' with date '+ date + ' ' + time + ' is obsolete. So we will skip it...'
                    instance.status = '1'
                    session.commit()
                    continue
                #endif                 

                loc_details = getDetailedInfo(place)
                if loc_details['status']==1:
                    #raw_input("Press Enter to continue...")
                    # FIXME - put this strange address into TBD_address table
                    print 'Note: ' + title + ' with place (' + place + ') is strange. So we will skip it...'
                    instance.status = '2'
                    session.commit()
                    continue
                #endif
                    
                print loc_details['formatted_address'].encode('utf-8')
                print loc_details['province'].encode('utf-8')
                print loc_details['city'].encode('utf-8')
                print loc_details['areaname'].encode('utf-8')
                print loc_details['areacode'].encode('utf-8')
                print loc_details['longitude']
                print loc_details['latitude']
            
                #wrap info into potentialItem
                potentialItem = {}
                potentialItem['source'] = to_unicode_or_bust(source)
                potentialItem['title'] = to_unicode_or_bust(title)
                potentialItem['desc'] = to_unicode_or_bust(desc)
                potentialItem['date'] = to_unicode_or_bust(date)
                potentialItem['time'] = to_unicode_or_bust(time)
                potentialItem['place'] = to_unicode_or_bust(place)
                potentialItem['fee'] = to_unicode_or_bust(fee)
                potentialItem['feelist'] = to_unicode_or_bust(feelist)
                potentialItem['imageurl'] = to_unicode_or_bust(imageurl)
                potentialItem['formatted_address'] = to_unicode_or_bust(loc_details['formatted_address'])
                potentialItem['province'] = to_unicode_or_bust(loc_details['province'])
                potentialItem['city'] = to_unicode_or_bust(loc_details['city'])
                potentialItem['areaname'] = to_unicode_or_bust(loc_details['areaname'])
                potentialItem['areacode'] = to_unicode_or_bust(loc_details['areacode'])
                potentialItem['longitude'] = to_unicode_or_bust(loc_details['longitude'])
                potentialItem['latitude'] = to_unicode_or_bust(loc_details['latitude'])
    
                # get all similar items (Q1) from search engine with criteria (query inputs)
                searchengine = Solr()
                # same - city, areacode, date, time
                q_areacode = 'areacode:' + loc_details['areacode']
                q_eventdate = 'eventdate:"' + date + '"'
                q_eventtime = 'eventtime:"' + time + '"'
                
                query = {}
                query['q'] = q_areacode.encode('utf-8') + ' AND ' + q_eventdate.encode('utf-8') +' AND ' + q_eventtime.encode('utf-8')
                # almost - keywords from title and description
                # FIXME, now we do not provide this feature

                # this flag used to turn on and turn off the duplicate removal feature
                #duplicate_removal = False;
                if(duplicate_removal==True):
                    # if len(Q1) == 0, regard this item as new item
                    Q1 = searchengine.process(query)
                    if ( len(Q1) == 0 ):
                        #put this item to lele repository
                        self.addToLeleRepository(potentialItem)
                    else: 
                        # if not, create WeixiaoTask to determine if it is a new item or not
                        self.createWeixiaoSimTask( potentialItem, Q1)
                        #raw_input("Press Enter to continue...")
                    #end if
                else:
                    print 'no duplicate removal feature ...'
                    self.addToLeleRepository(potentialItem)
                #endif

                # label this item as analyzed in the table of db - lelespider
                instance.status = '1'
                session.commit()

            #end for
        #end while

    #end def
 
    def addToLeleRepository(self, potentialItem):
        
        print 'begin to add to lele repository ... '
        # generate json item
        json_item = json.dumps(potentialItem)        
        print json_item
       
        # add this item use web service, FIXME
        #leleService.addItem(json_item)
        eventinfo = {}
        eventinfo['imageurl'] = potentialItem['imageurl'] 
        eventinfo['address'] = potentialItem['place']
        eventinfo['longitude'] = potentialItem['longitude']
        eventinfo['latitude'] = potentialItem['latitude']
        eventinfo['areacode'] = potentialItem['areacode']
        eventinfo['address_description'] = potentialItem['formatted_address']
        eventinfo['date'] = potentialItem['date']
        eventinfo['time'] = potentialItem['time']
        eventinfo['title'] = potentialItem['title']
        eventinfo['description'] = potentialItem['desc']
        eventinfo['fee_description'] = potentialItem['feelist']
        eventinfo['price'] = potentialItem['fee']
        eventinfo['fixnum'] = '100'
        print eventinfo

        url = self.url  #'http://wxlele.local/api/'
        eventinfo_json = json.dumps(eventinfo)
        info = urllib.urlencode({"AK":"robot.weixiao@1234567", "source":potentialItem['source'], "event":eventinfo_json})
        print info
        response = urllib2.urlopen(url, info).read()
        json_data = json.loads(response)
        print json_data['result']
        
        print 'end to add to lele repository ... '
        
    #end def

    def createWeixiaoSimTask(self, potentialItem, items):
        print 'begin createWeixiaoSimTask...'
        # create json string 
        json_task = json.dumps({'item':potentialItem, 'existing':items}, separators=(',',':'))
        print json_task 

        # and put it to lelesimtask table of lelespider, FIXME
        #WeixiaoTaskService.addSimTask(json_task)
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()

        new_task = {}
        new_task['jsontask'] = json_task
        new_task['date'] = potentialItem['date']
        new_task['time'] = potentialItem['time']
        new_task['same'] = False
        new_task['status'] = '0'

        simtask = SimTask(**new_task)
        session.add(simtask)
        session.commit()
        session.close()

        print 'end createWeixiaoSimTask...'

    #end def

#end class


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8') 
    print '[WeixiaoSim] - ' + 'WeixiaoSim starting ...'
   
    total = len(sys.argv)
    if(total != 2):
        print 'we need lele service url ... '
        sys.exit()
    #endif

    cmdargs = str(sys.argv)
    print ("Args list: %s " % sys.argv[1])

    wxSim = WeixiaoSim(sys.argv[1])
    wxSim.process()

#end if
