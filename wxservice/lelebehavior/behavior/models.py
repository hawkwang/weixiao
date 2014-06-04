#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship

import settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))
#enddef


def create_behaviors_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)
#enddef

class Behaviors(DeclarativeBase):
    """Sqlalchemy behaviors model"""
    __tablename__ = "behaviors"

    bid = Column(Integer, autoincrement=True, primary_key=True)
    uid = Column('uid', Integer, nullable=False)
    gid = Column('gid', Integer, nullable=False)
    t = Column('t', String, nullable=False)
    IP = Column('IP', String, nullable=False)
    bcode = Column('bcode', Integer, nullable=False)
    tcode = Column('tcode', Integer, nullable=False)
    tid = Column('tid', Integer, nullable=False)
#endclass


