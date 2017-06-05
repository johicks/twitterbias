import logging
from tweetorm import TweetDB
from tweetorm import Base
from textblob import TextBlob
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update

class TweetSentiment:

    def __init__(self):
        self.engine = create_engine('sqlite:///sqlalchemy_tweets.db')
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()


    def perform_sentiment_analysis(self):
        # Select all tweets from DB without sentiment score
        conn = self.engine.connect()
        result = self.session.query(TweetDB).filter(TweetDB.sentiment_polarity == None)
        for row in result:
            tweetblob = TextBlob(row.text)
            stmt = update(TweetDB).where(TweetDB.tweet_id==row.tweet_id).values(sentiment_polarity=tweetblob.polarity, sentiment_subjectivity=tweetblob.subjectivity)
            conn.execute(stmt)


if __name__ == '__main__':
    TS = TweetSentiment()
    TS.perform_sentiment_analysis()