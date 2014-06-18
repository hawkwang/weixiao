#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import *
import urllib

import settings

class Solr(object):

    def __init__(self):
        self.url_prefix = settings.SEARCHENGINE 
    #end def

    def process(self, query):
    
        print query
        realquery = urllib.urlencode(query)
        url = self.url_prefix + realquery
        print '[WeixiaoSim - Solr - process ] ' + url
        
        conn = urlopen(url)
        rsp = eval( conn.read() )
        print "number of matches=", rsp['response']['numFound']
        #print out the name field for each returned document
        resultlist = []
        for doc in rsp['response']['docs']:
            result = {}
            result['title'] = doc['title']
            result['address'] = doc['location_description'][0] + ' ' + doc['location_description'][1]
            resultlist.append(result)
            #print 'title field = ', result['title']
            #print 'location_description = ', result['address']
        #end for
        return resultlist
    #end def

#end class
