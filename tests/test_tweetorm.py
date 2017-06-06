# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlalchemy
import twitterbias.tweetorm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists


def test_tweetorm():
    engine = create_engine('sqlite:///sqlalchemy_tweets.db')
    twitterbias.tweetorm.Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    twitterbias.tweetorm.Base.metadata.create_all(engine)
    assert os.path.isfile('sqlalchemy_tweets.db')
    os.remove('sqlalchemy_tweets.db')

