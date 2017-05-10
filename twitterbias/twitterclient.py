"""Module to connect and interact with Twitter API"""
import configparser
import logging
import re
import tweepy

class TwitterClient():
    """Generic Twitter class to connect and interact with Twitter API"""

    def __init__(self):
        """Class constructor or initialization method"""
        self.get_twitter_credentials()
        self.try_twitter_auth()


    def get_twitter_credentials(self):
        """Parse twitterbias.cfg and pull Twitter API keys from TwitterClient section"""
        config = configparser.ConfigParser()
        config.read('twitterbias.cfg')
        self.consumer_key = config['TwitterClient']['consumer_key']
        self.consumer_secret = config['TwitterClient']['consumer_secret']
        self.access_token = config['TwitterClient']['access_token']
        self.access_token_secret = config['TwitterClient']['access_token_secret']


    def try_twitter_auth(self):
        try:
            # create OAuthHandler object
            self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            # set access token and secret
            self.auth.set_access_token(self.access_token, self.access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            self.api.me()
        except tweepy.error.TweepError as e:
            logging.error('TwitterClient returned: {0}'.format(e.reason))


    def clean_tweet(self, tweet):
        """Utility function to clean tweet text by removing links and special characters"""
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


if __name__ == '__main__':
    TC = TwitterClient()
