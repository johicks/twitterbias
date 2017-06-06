"""Module to visualize sentiment data into scatter charts"""
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
    """Generic class to connect to DB and visualize data"""

    def __init__(self, userids):
        """Class constructor or initialization method"""
        self.userids = userids
        self.engine = create_engine('sqlite:///sqlalchemy_{0}_{1}.db'.format(*userids))
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()


    def vis_data(self):
        """Query DB for userids(list) and assign polarity to x axis and subjectivity to y axis"""
        for userid in self.userids:
            x = []
            y = []
            df = pd.DataFrame()

            try:
                instance = self.session.query(TweetDB).filter(TweetDB.tweet_user_id == userid).all()
                for row in instance:
                    x.append(row.sentiment_polarity)
                    y.append(row.sentiment_subjectivity)
            except NoResultFound:
                logging.error('No tweets found in DB for @%s', userid)
            df['x'] = x
            df['y'] = y
            sns.lmplot('x', 'y',
                       data=df,
                       fit_reg=False,
                       scatter_kws={"marker": "D", "s": 100})
            plt.title('@{0}'.format(userid))
            plt.xlabel('Sentiment Polarity')
            plt.ylabel('Sentiment Subjectivity')
            plt.savefig('{0}.png'.format(userid))

if __name__ == '__main__':
    TV = TweetVis(['realDonaldTrump', 'HillaryClinton'])
    TV.vis_data()