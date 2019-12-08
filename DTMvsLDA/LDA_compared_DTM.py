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
    
def removeStopWords(messy_tweet):
    messy_tweet = messy_tweet.lower()
    refined_tweet = ' '.join([word for word in messy_tweet.split() if word not in cachedStopWords])
    return refined_tweet

def removeSpecialChar(orignal):
    final = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in orignal.split("\n")]
    return final

def remove2Char(tweet):
    new_tweet = ""
    for w in (" ".join(tweet)).split():
        if len(w) >= 3:
             new_tweet=new_tweet + w + " "
    return new_tweet

    
only_text = []
max_doc_size = 1000; count = 0
with open('ordered_day_hashtag_dtm.txt', mode = 'r') as f:
    csv_reader = csv.reader((x.replace('\0', '') for x in f), delimiter = ',')
    for row in csv_reader:
        only_text.append(remove2Char(removeSpecialChar(removeStopWords(removeURLs(row[2])))))
        count += 1
        if count == max_doc_size:
            break
 
docs = pytm.DocumentSet(only_text, min_df=5, max_df=0.5)

#Applying LDA on our dataset
n_topics = 20
lda = pytm.SVILDA(n_topics, docs.get_n_vocab())
lda.fit(docs, n_iteration=1000, B=1000, n_inner_iteration=5, n_hyper_iteration=20, J=5)

#Getting topic's and alpha values
topic_list = []
alphas = [lda.get_alpha(k) for k in range(n_topics)]
for k, alpha in enumerate(alphas):
    vocab = docs.get_vocab()
    phi = lda.get_phi(k)
    new_phi = np.around(list(phi), decimals = 3)
    #print('topic {0} (alpha = {1})'.format(k, np.around(alpha, decimals = 2)))
    a = sorted(zip(vocab, new_phi), key=lambda x: -x[1])[:10]
    topic_list.append(a)

total_training_time = time.time() - start_time

    
# Coverting topic into a excel file
print("Putting in DataFrame started")
df = pd.DataFrame(topic_list)
writer = pd.ExcelWriter("1000docs_20topics_LDA.xlsx")
df.to_excel(writer, 'Topics')

df1 = pd.DataFrame([[total_training_time, "Seconds"]])
df1.to_excel(writer, 'TrainingTime')
writer.save()