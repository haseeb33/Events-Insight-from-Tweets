#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 16:38:04 2019

@author: khan
"""

import csv
#global dictonary for hashtags and tweets
All_hashtags = {}
All_hashtag_count = {}

def removeHashtags(tweet):
    ls_tweet = tweet.split()
    hashtags = []
    for word in ls_tweet:
        if word[0] == "#":
            hashtags.append(word[1:])
    if hashtags:
        for tag in hashtags:            
            ls_tweet.remove("#" + tag)
    return hashtags, " ".join(ls_tweet)
    
def detectHashtag(tweet):
    hashtags, new_tweet = removeHashtags(tweet)
    if hashtags:
        for tag in hashtags:
            if tag in All_hashtags.keys():
                All_hashtags[tag] = All_hashtags[tag] + " " + new_tweet
                All_hashtag_count[tag] += 1
            else:
                All_hashtags[tag] = new_tweet
                All_hashtag_count[tag] = 1
              
    
tweets = []
with open('english_tweets.txt', mode = 'r') as f:
    csv_reader = csv.reader((x.replace('\0', '') for x in f), delimiter = ',')
    for row in csv_reader:
        tweets.append(row[1])

for tweet in tweets:
    detectHashtag(tweet)

with open("hashtag_pooled_tweets.txt", mode = 'w') as f:
    csv_f = csv.writer(f, delimiter=',')
    for key in All_hashtags.keys():
        csv_f.writerow([key, All_hashtags[key]])
