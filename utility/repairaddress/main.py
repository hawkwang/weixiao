#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import sys
import re
from sqlalchemy.orm import sessionmaker, relationship
from models import db_connect, create_tables
from models import Faddress, Address



def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj
#end def

f = open("address.txt",'r')
lines = f.readlines() # will append in the list lines

for line in lines:
    print (to_unicode_or_bust(line)).encode('utf-8')
    line = re.sub('"', '', line)
    line = re.sub('\n', '', line)
    fields = line.split( ';' )

    address = 	(to_unicode_or_bust(fields[0])).encode('utf-8')
    fid = 	(to_unicode_or_bust(fields[1])).encode('utf-8')
    formatted_address = (to_unicode_or_bust(fields[2])).encode('utf-8')
    province = 	(to_unicode_or_bust(fields[3])).encode('utf-8')
    city = 	(to_unicode_or_bust(fields[4])).encode('utf-8')
    areaname = 	(to_unicode_or_bust(fields[5])).encode('utf-8')
    areacode = 	(to_unicode_or_bust(fields[6])).encode('utf-8')
    longitude = (to_unicode_or_bust(fields[7])).encode('utf-8')
    latitude = 	(to_unicode_or_bust(fields[8])).encode('utf-8')

    print address
    hash_object = hashlib.md5(address)
    aid = hash_object.hexdigest()
    print aid

    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    # get the Address info from lelespider
    for address in session.query(Address).filter(Address.aid==aid):
        address.fid = fid
        session.commit()
    #endfor

    # get the Faddress info from lelespider
    for faddress in session.query(Faddress).filter(Faddress.fid==fid):
        faddress.formatted_address = formatted_address
        faddress.province = province
        faddress.city = city
        faddress.areaname = areaname
        faddress.areacode = areacode
        faddress.longitude = longitude
        faddress.latitude = latitude
        session.commit()
    #endfor

#endfor

    


