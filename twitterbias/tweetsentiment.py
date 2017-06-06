import logging
from tweetorm import TweetDB
from tweetorm import Base
from textblob import TextBlob
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update

class TweetSentiment:

    def __init__(self, userids):
        self.userids = userids
        self.engine = create_engine('sqlite:///sqlalchemy_{0}_{1}.db'.format(*self.userids))
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
            logging.debug('Inserted new sentiment analysis for user %s tweet ID %s', row.tweet_user_id, row.tweet_id)


if __name__ == '__main__':
    TS = TweetSentiment(['realDonaldTrump', 'HillaryClinton'])
    TS.perform_sentiment_analysis()