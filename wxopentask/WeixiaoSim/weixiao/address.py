#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import *
from sqlalchemy.orm import sessionmaker, relationship
from models import db_connect, create_events_table
from models import Events, Faddress, Address
from leletext import to_unicode_or_bust
import hashlib
import time
import pytz
from datetime import tzinfo, timedelta, datetime
import sys
import map.baidumap


def getDetailedInfo(address, city=u'北京市'):

    address = address.replace(' ','')
        
    detailinfo = {}
    detailinfo['status'] = 1
    detailinfo['formatted_address'] = ''
    detailinfo['province'] = ''
    detailinfo['city'] = ''
    detailinfo['areaname'] = ''
    detailinfo['areacode'] = ''
    detailinfo['longitude'] = ''
    detailinfo['latitude'] = ''

    hash_object = hashlib.md5((to_unicode_or_bust(address)).encode('utf-8'))
    aid = hash_object.hexdigest()
    acity = city

    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    # get the address info from lelespider
    addresses = session.query(Address).filter(Address.aid==aid).filter(Address.city==acity).all()
    
    # if the detailed info can be found in lelespider db, just return to client
    length = len(addresses)
    if (length==1):
        address = addresses[0]
        fid = address.fid
        if (fid==None):
            session.close()
            return detailinfo
        else:
            # get detailed info from faddress table (FIXME, faddress can be return null)
            faddress = session.query(Faddress).filter_by(fid=fid).one()
            detailinfo['status'] = 0
            detailinfo['formatted_address'] = to_unicode_or_bust(faddress.formatted_address)
            detailinfo['province'] = to_unicode_or_bust(faddress.province)
            detailinfo['city'] = to_unicode_or_bust(faddress.city)
            detailinfo['areaname'] = to_unicode_or_bust(faddress.areaname)
            detailinfo['areacode'] = to_unicode_or_bust(faddress.areacode)
            detailinfo['longitude'] = to_unicode_or_bust(faddress.longitude)
            detailinfo['latitude'] = to_unicode_or_bust(faddress.latitude)
            
            session.close()
            return detailinfo
        #endif
    #endif

    # no information from lelespider db, so we need to get address detail from baidu or google map service 
    place = address
    loc_details = map.baidumap.getDetailedInfo(place)
    if loc_details['status']==1:
        place = u'北京市' + address
        print 'try again with ' + place.encode('utf-8')
        loc_details = map.baidumap.getDetailedInfo(place)
    #endif
    if loc_details['status']==1:
        place = u'北京' + address
        print 'try again with ' + place.encode('utf-8')
        loc_details = map.baidumap.getDetailedInfo(place)
    #endif
    if loc_details['status']==1:
        place = u'北京市 ' + address
        print 'try again with ' + place.encode('utf-8')
        loc_details = map.baidumap.getDetailedInfo(place)
    #endif
    if loc_details['status']==1:
        place = u'北京 ' + address
        print 'try again with ' + place.encode('utf-8')
        loc_details = map.baidumap.getDetailedInfo(place)
    #endif
    # if no detailed information can be found throught baidu or google service,
    # just put this address info to address table with out None value for 
    # field fid, which is eventually will be solved manually or by WeixiaoTask 
    # approach
    if loc_details['status']==1:
        # put address item with None fid
        new_address = {}
        new_address['aid'] = aid
        new_address['city'] = acity
        new_address['address'] = address
        new_address['created'] = datetime.utcnow().isoformat(' ')
        address_item = Address(**new_address)
        session.add(address_item)
        session.commit()
        session.close()
        return detailinfo;
    #endif
        
    # put this info
    new_faddress = {}
    new_faddress['formatted_address'] = to_unicode_or_bust(loc_details['formatted_address'])
    new_faddress['province'] = to_unicode_or_bust(loc_details['province'])
    new_faddress['city'] = to_unicode_or_bust(loc_details['city'])
    new_faddress['areaname'] = to_unicode_or_bust(loc_details['areaname'])
    new_faddress['areacode'] = to_unicode_or_bust(loc_details['areacode'])
    new_faddress['longitude'] = to_unicode_or_bust(loc_details['longitude'])
    new_faddress['latitude'] = to_unicode_or_bust(loc_details['latitude'])
    
    faddress_item = Faddress(**new_faddress)
    session.add(faddress_item)
    session.commit() 
    session.refresh(faddress_item)
    fid = faddress_item.fid

    # put address item with None fid
    new_address = {}
    new_address['aid'] = aid
    new_address['city'] = acity
    new_address['address'] = address
    new_address['created'] = datetime.utcnow().isoformat(' ')
    new_address['fid'] = fid
    address_item = Address(**new_address)
    session.add(address_item)
    session.commit()    

    detailinfo['status'] = 0
    detailinfo['formatted_address'] = to_unicode_or_bust(loc_details['formatted_address'])
    detailinfo['province'] = to_unicode_or_bust(loc_details['province'])
    detailinfo['city'] = to_unicode_or_bust(loc_details['city'])
    detailinfo['areaname'] = to_unicode_or_bust(loc_details['areaname'])
    detailinfo['areacode'] = to_unicode_or_bust(loc_details['areacode'])
    detailinfo['longitude'] = to_unicode_or_bust(loc_details['longitude'])
    detailinfo['latitude'] = to_unicode_or_bust(loc_details['latitude'])

    session.close()
    return detailinfo

#enddef
