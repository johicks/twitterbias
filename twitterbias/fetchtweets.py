import logging
import twitterclient
import tweetorm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sqlalchemy_tweets.db')
tweetorm.Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def create_if_not_exists(session, twitteruser, model):
    TC = twitterclient.TwitterClient()
    tweets = TC.api.user_timeline(screen_name=twitteruser, count=200)
    for tweet in tweets:
        instance = session.query(model).filter(model.tweet_id == tweet.id).one()
        if instance:
            logging.debug('Tweet ID exists in DB, skipping: %s', tweet.id)
        else:
            new_tweet = model(
                created_at=tweet.created_at,
                text=TC.clean_tweet(tweet.text),
                tweet_id=tweet.id
                )
            session.add(new_tweet)
            session.commit()

if __name__ == '__main__':            
    create_if_not_exists(session, 'realDonaldTrump', tweetorm.Trump)
    create_if_not_exists(session, 'HillaryClinton', tweetorm.Clinton)
