#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

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


