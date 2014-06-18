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

class Faddress(DeclarativeBase):
    """Sqlalchemy Faddress model"""
    __tablename__ = "faddress"

    fid = Column(Integer, autoincrement=True, primary_key=True)
    formatted_address = Column('formatted_address', String)
    province = Column('province', String)
    city = Column('city', String)
    areaname = Column('areaname', String)
    areacode = Column('areacode', String)
    longitude = Column('longitude', String)
    latitude = Column('latitude', String)
    addresses = relationship("Address", order_by="desc(Address.address)", primaryjoin="Address.fid==Faddress.fid")
#end class

class Address(DeclarativeBase):
    """Sqlalchemy Address model"""
    __tablename__ = "address"

    aid = Column('aid', String, primary_key=True)
    city = Column('city', String, primary_key=True)
    address = Column('address', String, nullable=False)
    faddress = Column('faddress', String, nullable=False)
    fid = Column(Integer, ForeignKey('faddress.fid'))
    faddress = relationship(Faddress, primaryjoin=fid == Faddress.fid)
#end class

class SimTask(DeclarativeBase):
    """Sqlalchemy SimTask model"""
    __tablename__ = "simtask"

    tid = Column(Integer, autoincrement=True, primary_key=True)
    jsontask = Column('jsontask', String, nullable=False)
    date = Column('date', String, nullable=False)
    time = Column('time', String, nullable=False)
    same = Column('same', Boolean, nullable=False)
    status = Column('status', String, nullable=False)
    
#end class

