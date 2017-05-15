"""Module to create DB tables to store Tweets"""
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()

class Trump(Base):
    __tablename__ = 'trump'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime())
    text = Column(String(250), nullable=False)
    semantic_score = Column(Integer)
    tweet_id = Column(Integer)

class Clinton(Base):
    __tablename__ = 'clinton'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime())
    text = Column(String(250), nullable=False)
    semantic_score = Column(Integer)
    tweet_id = Column(Integer)

engine = create_engine('sqlite:///sqlalchemy_tweets.db')

Base.metadata.create_all(engine)