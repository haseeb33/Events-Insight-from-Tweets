#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 19:52:23 2018

@author: khan
"""

import pytm
import csv
import numpy as np
from nltk.corpus import stopwords
import re
import sys
import pandas as pd
import time

start_time = time.time()

csv.field_size_limit(sys.maxsize)

cachedStopWords = stopwords.words("english")

def removeURLs(tweet):
    return re.sub(r'http\S+', '', tweet)

def removeUsernames(tweet):
    return re.sub(r'@\S+', '', tweet)


def removeStopWords(messy_tweet):
    messy_tweet = messy_tweet.lower()
    refined_tweet = ' '.join([word for word in messy_tweet.split() if word not in cachedStopWords])
    return refined_tweet

def removeSpecialChar(orignal):
    return re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in orignal.split("\n")

def remove2Char(tweet):
    new_tweet = ""
    for w in tweet.split():
        if len(w) >= 3:
             new_tweet=new_tweet + w + " "
    return new_tweet

only_text = []
with open('all_english_tweets.txt', mode = 'r') as f:
    csv_reader = csv.reader((x.replace('\0', '') for x in f), delimiter = ',')
    for row in csv_reader:
        only_text.append(remove2Char(removeSpecialChar(removeStopWords(removeUsernames(removeURLs(row[1]))))))

docs = pytm.DocumentSet(only_text, min_df=5, max_df=0.5)

#Applying LDA on our dataset
n_topics = 1000
lda = pytm.SVILDA(n_topics, docs.get_n_vocab())
lda.fit(docs, n_iteration=1000, B=1000, n_inner_iteration=5, n_hyper_iteration=20, J=5)

#Getting topic's and alpha values
topic_list = []
alphas = [lda.get_alpha(k) for k in range(n_topics)]
for k, alpha in enumerate(alphas):
    vocab = docs.get_vocab()
    phi = lda.get_phi(k)
    new_phi = np.around(list(phi), decimals = 3)
    print('topic {0} (alpha = {1})'.format(k, np.around(alpha, decimals = 2)))
    a = sorted(zip(vocab, new_phi), key=lambda x: -x[1])[:10]
    print(a)
    topic_list.append(a)

total_training_time = time.time() - start_time

print(total_training_time)

start_time1 = time.time()
#getting theta for one doc and checking
hashtag_text = []
hashtag_name_count = []
with open("day_#_morethan3tweets.txt", mode = "r") as f1:
    csv_r = csv.reader((x.replace('\0', '') for x in f1), delimiter = ',')
    for row in csv_r:
        t = remove2Char(removeSpecialChar(removeStopWords(removeUsernames(removeURLs(row[2])))))
        if len(t) >= 3:
            hashtag_text.append(t)
            hashtag_name_count.append([row[0], row[1]])

print("Hashtag text lists created: LDA get theta started")
docs1 = pytm.DocumentSet(hashtag_text, min_df=5, max_df=0.5)
theta1 = lda.get_theta(docs1)
print("Got theta values")

empty_text_entries = [i for i, e in enumerate(hashtag_text) if e == ""]
for entry in range((len(empty_text_entries)-1), -1, -1):
    del hashtag_text[empty_text_entries[entry]]
    del hashtag_name_count[empty_text_entries[entry]]

# Coverting topic into a excel file
print("Putting in DataFrame started")
df = pd.DataFrame(topic_list)
writer = pd.ExcelWriter("1000_topics_morethan3tweets_#.xlsx")
df.to_excel(writer, 'Sheet1')

df1 = pd.DataFrame(theta1)
df1.to_excel(writer, 'Sheet2')

df2 = pd.DataFrame(hashtag_name_count)
df2.to_excel(writer, 'Sheet3')
writer.save()

total_testing_time = time.time() - start_time1
print(total_testing_time)
