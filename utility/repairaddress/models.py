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


def create_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


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


