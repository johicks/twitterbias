import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tweetorm import TweetDB
from tweetorm import Base
from textblob import TextBlob
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


class TweetVis:

    def __init__(self):
        self.engine = create_engine('sqlite:///sqlalchemy_tweets.db')
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def vis_trump_data(self):
        x = []
        y = []
        df = pd.DataFrame()

        try:
            instance = self.session.query(TweetDB).filter(TweetDB.tweet_user_id == 'realDonaldTrump').all()
            for row in instance:
                x.append(row.sentiment_polarity)
                y.append(row.sentiment_subjectivity)
        except NoResultFound:
            logging.error('No tweets found in DB for @realDonaldTrump')
        df['x'] = x
        df['y'] = y
        sns.lmplot('x', 'y',
                   data=df,
                   fit_reg=False,
                   scatter_kws={"marker": "D", "s": 100})
        plt.title('@realDonaldTrump')
        plt.xlabel('Sentiment Polarity')
        plt.ylabel('Sentiment Subjectivity')
        plt.savefig('trump.png')

    
    def vis_clinton_data(self):
        x = []
        y = []
        df = pd.DataFrame()

        try:
            instance = self.session.query(TweetDB).filter(TweetDB.tweet_user_id == 'HillaryClinton').all()
            for row in instance:
                x.append(row.sentiment_polarity)
                y.append(row.sentiment_subjectivity)
        except NoResultFound:
            logging.error('No tweets found in DB for @realDonaldTrump')
        df['x'] = x
        df['y'] = y
        sns.lmplot('x', 'y',
                   data=df,
                   fit_reg=False,
                   scatter_kws={"marker": "D", "s": 100})
        plt.title('@HillaryClinton')
        plt.xlabel('Sentiment Polarity')
        plt.ylabel('Sentiment Subjectivity')
        plt.savefig('clinton.png')

if __name__ == '__main__':
    tweetvis = TweetVis()
    tweetvis.vis_trump_data()
    tweetvis.vis_clinton_data()