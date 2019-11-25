#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:03:24 2018

@author: khan
"""
import json
# Library to detect the language of tweet
from langdetect import detect
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import csv
import glob

lines = []
nu = 0
for idx, filename in enumerate(glob.glob('*.json')):
    print(filename, str(idx))
    with open(filename, encoding = "utf-8", mode = "r") as f:
        lines.append(f.readlines())
 
tweets = []   
for line in lines:
    for l in line:
        tweets.append(json.loads(l))

#From all tweet2011 data getting only tweets text and date 
date_text = []
for tweet in tweets:
    date_text.append([tweet["text"], tweet["created_at"]])
    
    
english_tweets = []
other_tweets = []

#APPLY LANDETECT AND FIND ONLY ENGLISH TWEETS
for dt in date_text:
    try:
        if detect(dt[0]) == 'en':
            #Appending the english tweets
            english_tweets.append(dt)
        else:
            #Appending tweets of other languages
            other_tweets.append(dt) 
    except:
        print(dt[0])
         
#Creating english tweets txt file in csv formate
with open("english_tweets.txt", mode = 'w') as f:
    csv_f = csv.writer(f, delimiter=',')
    for et in english_tweets:
        csv_f.writerow([et[1], et[0]])
    