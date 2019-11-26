#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 17:32:51 2019

@author: khan
"""

import os
import csv
import shutil

#global dictonary for hashtags and count
Day_hashtags = {}
Day_hashtag_count = {}

def removeHashtags(tweet, date):
    ls_tweet = tweet.split()
    ls_tweet = [x.lower() for x in ls_tweet]
    hashtags = []
    for word in ls_tweet:
        if word[0] == "#":
            hashtags.append(word[1:])
    if hashtags:
        for tag in hashtags:
            ls_tweet.remove("#" + tag)
    return [tag + date for tag in hashtags], " ".join(ls_tweet)

def detectHashtag(tweet, date):
    hashtags, new_tweet = removeHashtags(tweet, date)
    if hashtags:
        for tag in hashtags:
            if tag in Day_hashtags.keys():
                Day_hashtags[tag] = Day_hashtags[tag] + " " + new_tweet
                Day_hashtag_count[tag] += 1
            else:
                Day_hashtags[tag] = new_tweet
                Day_hashtag_count[tag] = 1

tweets = []
dates = []
with open('english_tweets.txt', mode = 'r') as f:
    csv_reader = csv.reader((x.replace('\0', '') for x in f), delimiter = ',')
    for row in csv_reader:
        tweets.append(row[1])
        date_time = row[0].split()
        dates.append("_" + date_time[1] + "_" + date_time[2] + "_" + date_time[5])

for tweet, date in zip(tweets, dates):
    detectHashtag(tweet, date)

# Create a directory and store one hashtag as one file: file formate = tag_date_count
"""
dirName = "Day_hashtag"
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:
    shutil.rmtree(dirName)
    os.mkdir(dirName)
    print("Directory " , dirName ,  " deleted and created newly")

for tag in Day_hashtags.keys():
    count = Day_hashtag_count[tag]
    if count >10:
        current_directory = os.getcwd() + "/" + dirName
        try:
            with open(os.path.join(current_directory , tag + "_" + str(count) + ".txt"), mode = 'w') as f:
                #csv_writer = csv.writer(f, delimiter = ',')
                f.write(Day_hashtags[tag])
        except:
            None
"""
#Change the variable based on your requirement
create_if_tweets_are_more_than = 3
with open("day_#_morethan3tweets.txt", mode = 'w') as f:
    csv_f = csv.writer(f, delimiter=',')
    for key in Day_hashtags.keys():
        if Day_hashtag_count[key] >= create_if_tweets_are_more_than:
            csv_f.writerow([key, Day_hashtag_count[key], Day_hashtags[key]])
