import logging
import twitterclient
import tweetorm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


class FetchTweets:

    def __init__(self):
        self.engine = create_engine('sqlite:///sqlalchemy_tweets.db')
        tweetorm.Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()


    def create_if_not_exists(self, twitteruser, model):
        twitterc = twitterclient.TwitterClient()
        tweets = twitterc.api.user_timeline(screen_name=twitteruser, count=200)
        for tweet in tweets:
            try:
                instance = self.session.query(model).filter(model.tweet_id == tweet.id).one()
                if instance:
                    logging.debug('Tweet ID from user %s exists in DB, skipping: %s', twitteruser, tweet.id)
            except NoResultFound:
                new_tweet = model(
                    tweet_user_id=twitteruser,
                    created_at=tweet.created_at,
                    text=twitterc.clean_tweet(tweet.text),
                    tweet_id=tweet.id
                    )
                self.session.add(new_tweet)
                self.session.commit()


if __name__ == '__main__':
    FC = FetchTweets()
    FC.create_if_not_exists('realDonaldTrump', tweetorm.TweetDB)
    FC.create_if_not_exists('HillaryClinton', tweetorm.TweetDB)
