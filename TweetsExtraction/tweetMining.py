#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 18:04:53 2020

@author: khan
"""

import tweepy
import numpy as np
import pandas as pd
import json

with open('api_key_file.json') as json_file:
    data = json.load(json_file)

access_token = data["access_key"]
access_token_secret = data["access_secret"]
consumer_key = data["api_key"]
consumer_secret = data["api_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweets = []
for tweet in api.search('food'):
    tweets.append(tweet)
    print(tweet.text)