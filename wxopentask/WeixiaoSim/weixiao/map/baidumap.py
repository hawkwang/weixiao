#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

def get_areacode_by_areaname(areaname):
    area = {}
    area[u'东城区'] = '110101'
    area[u'西城区'] = '110102'
    area[u'崇文区'] = '110103'
    area[u'宣武区'] = '110104'
    area[u'朝阳区'] = '110105'
    area[u'丰台区'] = '110106'
    area[u'石景山区'] = '110107'
    area[u'海淀区'] = '110108'
    area[u'门头沟区'] = '110109'
    area[u'房山区'] = '110111'
    area[u'通州区'] = '110112'
    area[u'顺义区'] = '110113'
    area[u'昌平区'] = '110114'
    area[u'大兴区'] = '110115'
    area[u'怀柔区'] = '110116'
    area[u'平谷区'] = '110117'
    area[u'密云县'] = '110228'
    area[u'延庆县'] = '110229'
    code = area.get(areaname, '0')
    return code
#enddef

# FIXME - loc_details should include one field to indicate if this address 
# is get from our own address service or from baidu or google map service

# if this address is newly found by baidu map or google map service, 
# we need to add it to our own address database for future usage

def getDetailedInfo(address, city=u'北京市'):

    detailinfo = {} 
    detailinfo['status'] = 1
    detailinfo['formatted_address'] = ''
    detailinfo['province'] = ''
    detailinfo['city'] = ''
    detailinfo['areaname'] = ''
    detailinfo['areacode'] = ''
    detailinfo['longitude'] = ''
    detailinfo['latitude'] = ''
    
    flag = True
    map_api_url = 'http://api.map.baidu.com/geocoder/v2/'
    url = map_api_url + '?output=json&ak=HL2OtpqEFglWT1j2RoS62eRD' + '&address=' + address.encode('utf-8') + '&city=' + city.encode('utf-8')
    print url
    headers = {'content-type': 'application/json'}
    r = requests.get(url)
    if r.status_code / 100 == 2:
        if r.text and r.text != '""':
            resp = json.loads(r.text)
        else:
            flag = False
        #end if
    else:
        flag = False
    #end if
    if flag==False:
        return detailinfo
    #end if
    if(resp['status']==0):
        try:    
            lat = resp['result']['location']['lat']
            lng = resp['result']['location']['lng']
        except:
            return detailinfo
    else:
        return detailinfo
    #end if
    
    url = map_api_url + '?output=json&ak=HL2OtpqEFglWT1j2RoS62eRD' + '&location=' + str(lat) + ',' + str(lng)
    r = requests.get(url)
    resp = json.loads(r.text)
    if resp['status']==0:
        
        addressComponent = resp['result']['addressComponent']
        
        province = addressComponent['province']
        city = addressComponent['city']
        areaname = addressComponent['district']
        formatted_address = resp ['result']['formatted_address']
        #get areacode,FIXME
        areacode = get_areacode_by_areaname(areaname)
        
        # wrap detailinfo
        detailinfo['status'] = 0
        detailinfo['formatted_address'] = formatted_address
        detailinfo['province'] = province
        detailinfo['city'] = city
        detailinfo['areaname'] = areaname
        detailinfo['areacode'] = areacode
        detailinfo['longitude'] = lng
        detailinfo['latitude'] = lat

        return detailinfo
    #end if

    return detailinfo
#end def
