# -*- coding: utf-8 -*-
import sys
import os
import tweepy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import twitterbias.twitterclient

def test_twitter_auth():
    TC = twitterbias.twitterclient.TwitterClient()
    assert type(TC.api.me()) is tweepy.models.User
