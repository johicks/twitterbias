"""Module to create DB tables to store Tweets"""
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()

class TweetDB(Base):
    __tablename__ = 'tweetdb'
    tweet_id = Column(Integer, primary_key=True)
    tweet_user_id = Column(String(250), nullable=False)
    created_at = Column(DateTime())
    text = Column(String(250), nullable=False)
    sentiment_polarity = Column(Integer)
    sentiment_subjectivity = Column(Integer)

engine = create_engine('sqlite:///sqlalchemy_tweets.db')

Base.metadata.create_all(engine)
