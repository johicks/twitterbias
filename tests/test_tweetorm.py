# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlalchemy
import twitterbias.tweetorm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def test_tweetorm():
    engine = create_engine('sqlite:///sqlalchemy_tweets.db')
    twitterbias.tweetorm.Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    assert os.path.isfile('sqlalchemy_tweets.db')
    os.remove('sqlalchemy_tweets.db')

