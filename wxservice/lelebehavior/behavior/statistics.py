#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker, relationship
from models import db_connect, create_behaviors_table
from models import Behaviors

def getbrief(query):
    report = {}
    report['self'] = 0;
    report['total'] = 0;

    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    myquery = session.query(Behaviors)
    myquery = myquery.filter(Behaviors.tcode==query['tcode'])
    myquery = myquery.filter(Behaviors.tid==query['tid'])

    total = getTotal(query, myquery)
    self = getSelf(query, myquery)
    
    report['self'] = self
    report['total'] = total

    return report
#enddef


def getTotal(query, mysqlquery):
    
    myquery = mysqlquery
    #determine if we need to get all the group related behaviors
    if(query['gid']>=-1):
        myquery = myquery.filter(Behaviors.gid==query['gid'])
    #endif
    # deal with behavior type
    # for 'like'
    if(query['bcode']==4):
        #get 4 count
        myfirstquery = myquery.filter(Behaviors.bcode==4)
        #get 5 count
        mysecondquery = myquery.filter(Behaviors.bcode==5)
        # get the total count of like 
        total_count = myfirstquery.count() - mysecondquery.count()
        return total_count
    #endif

    # for 'care'
    if(query['bcode']==10):
        #get 10 count
        myfirstquery = myquery.filter(Behaviors.bcode==10)
        #get 11 count
        mysecondquery = myquery.filter(Behaviors.bcode==11)
        # get the total count of care
        total_count = myfirstquery.count() - mysecondquery.count()
        return total_count
    #endif

    myquery = myquery.filter(Behaviors.bcode==query['bcode'])
    total_count = myquery.count()
    return total_count
#enddef

def getSelf(query, mysqlquery):

    myquery = mysqlquery
    #determine if we need to get all the user related behaviors
    if(query['uid']>=-1):
        myquery = myquery.filter(Behaviors.uid==query['uid'])
    else:
        return 0
    #endif
    #determine if we need to get all the group related behaviors
    if(query['gid']>=-1):
        myquery = myquery.filter(Behaviors.gid==query['gid'])
    #endif
    # deal with behavior type
    if(query['bcode']==4):
        #get 4 count
        myfirstquery = myquery.filter(Behaviors.bcode==4)
        #get 5 count
        mysecondquery = myquery.filter(Behaviors.bcode==5)
        # get the total count of like 
        self_count = myfirstquery.count() - mysecondquery.count()
        return self_count
    #endif

    if(query['bcode']==10):
        #get 4 count
        myfirstquery = myquery.filter(Behaviors.bcode==10)
        #get 5 count
        mysecondquery = myquery.filter(Behaviors.bcode==11)
        # get the total count of care 
        self_count = myfirstquery.count() - mysecondquery.count()
        return self_count
    #endif

    myquery = myquery.filter(Behaviors.bcode==query['bcode'])
    self_count = myquery.count()
    return self_count
#enddef

