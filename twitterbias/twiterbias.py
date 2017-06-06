import argparse
import logging
import os
import fetchtweets
import tweetsentiment
import tweetvis
from tweetorm import TweetDB


def SilentRemove(filename):
    """Delete local file and fails silently if file not found."""
    try:
        os.remove(filename)
        ROOT.info('Deleted local file %s', filename)
    except FileNotFoundError:
        ROOT.debug('Failed to delete %s', filename)


if __name__ == '__main__':

    ROOT = logging.getLogger()
    ROOT.setLevel(logging.WARN)

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-v', dest='verbose', action='store_true',
                        help='Enables logging output to console of debug events')
    PARSER.add_argument('-n', dest='new_db', action='store_true',
                        help='Performs a clean semantic analysis by wiping existing DB')

    ARGS = PARSER.parse_args()

    if ARGS.verbose:
        ROOT.setLevel(logging.DEBUG)

    if ARGS.new_db:
        SilentRemove('sqlalchemy_tweets.db')

    FT = fetchtweets.FetchTweets()
    FT.create_if_not_exists('realDonaldTrump', TweetDB)
    FT.create_if_not_exists('HillaryClinton', TweetDB)
    TS = tweetsentiment.TweetSentiment()
    TS.perform_sentiment_analysis()
    TV = tweetvis.TweetVis()
    TV.vis_trump_data()
    TV.vis_clinton_data()
