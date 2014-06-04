#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker, relationship
from models import db_connect, create_behaviors_table
from models import Behaviors
import threading

class behavior (threading.Thread):
    def __init__(self, obj):
        threading.Thread.__init__(self)
        self.engine = db_connect()
        create_behaviors_table(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.obj = obj
    #end def

    def run(self):
        # put behavior item into the database
        try:
            behavior_item = Behaviors(**self.obj)
            self.session.add(behavior_item)
            self.session.commit() 
            self.session.close()
            print 'ok to save behavior'
        except Exception as e:
            print str(e)
        #endtry
    #enddef

#end class




