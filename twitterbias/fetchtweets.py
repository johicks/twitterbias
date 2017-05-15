import twitterclient
import tweetorm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sqlalchemy_tweets.db')

tweetorm.Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

TC = twitterclient.TwitterClient()
tweets = TC.api.user_timeline(screen_name='realDonaldTrump', count=200)
for tweet in tweets:
    new_tweet = tweetorm.Trump(
        created_at=tweet.created_at,
        text=TC.clean_tweet(tweet.text),
        tweet_id=tweet.id
        )

    session.add(new_tweet)
    session.commit()

tweets = TC.api.user_timeline(screen_name='HillaryClinton', count=200)
for tweet in tweets:
    new_tweet = tweetorm.Clinton(
        created_at=tweet.created_at,
        text=TC.clean_tweet(tweet.text),
        tweet_id=tweet.id
        )

    session.add(new_tweet)
    session.commit()