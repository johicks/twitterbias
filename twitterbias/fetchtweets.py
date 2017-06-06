import logging
import twitterclient
import tweetorm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


class FetchTweets:

    def __init__(self, userids):
        self.userids = userids
        self.engine = create_engine('sqlite:///sqlalchemy_{0}_{1}.db'.format(*self.userids))
        tweetorm.Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()


    def create_if_not_exists(self, model=tweetorm.TweetDB):
        twitterc = twitterclient.TwitterClient()
        for userid in self.userids:
            tweets = twitterc.api.user_timeline(screen_name=userid, count=200)
            for tweet in tweets:
                try:
                    instance = self.session.query(model).filter(model.tweet_id == tweet.id).one()
                    if instance:
                        logging.debug('Tweet ID from user %s exists in DB, skipping: %s', userid, tweet.id)
                except NoResultFound:
                    new_tweet = model(
                        tweet_user_id=userid,
                        created_at=tweet.created_at,
                        text=twitterc.clean_tweet(tweet.text),
                        tweet_id=tweet.id
                        )
                    self.session.add(new_tweet)
                    self.session.commit()
                    logging.debug('Added new Tweet from user %s with ID %s', userid, tweet.id)


if __name__ == '__main__':
    FT = FetchTweets(['realDonaldTrump', 'HillaryClinton'])
    FT.create_if_not_exists()
