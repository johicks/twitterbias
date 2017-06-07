"""Command line client to perform sentiment analysis of two twitter users"""
import argparse
import logging
import fetchtweets
import tweetsentiment
import tweetvis
import tweetorm


if __name__ == '__main__':

    ROOT = logging.getLogger()
    ROOT.setLevel(logging.WARN)

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-v', dest='verbose', action='store_true',
                        help='Enables logging output to console of debug events')
    PARSER.add_argument('-users', required=True, nargs='*',
                        help='Twitter users to perform sentiment analysis on')

    ARGS = PARSER.parse_args()

    if ARGS.verbose:
        ROOT.setLevel(logging.DEBUG)

    if len(ARGS.users) < 2:
        print('ERROR: -users requires 2 arguments')
    elif len(ARGS.users) > 2:
        print('ERROR: -users takes a maximum of 2 arguments')
    else:
        # Create DB if it doesn't already exist
        tweetorm.create_db(ARGS.users)

        # Fetch last 200 tweets for each user and insert them into DB if not already present
        FT = fetchtweets.FetchTweets(ARGS.users)
        FT.create_if_not_exists()

        # Query DB for tweets without sentiment analysis, perform analsysis, insert result into DB
        TS = tweetsentiment.TweetSentiment(ARGS.users)
        TS.perform_sentiment_analysis()

        # Generate charts for each users sentiment data
        TV = tweetvis.TweetVis(ARGS.users)
        TV.vis_data()
