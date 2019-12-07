#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 17:19:59 2019

@author: khan
"""
from gensim.test.utils import common_corpus, common_dictionary
from gensim.models.wrappers import DtmModel
from gensim import corpora
import csv
from nltk.corpus import stopwords
import re
import sys
import time
from collections import defaultdict
import pandas as pd

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

documents = []
with open('all_english_tweets.txt', mode = 'r') as f:
    csv_reader = csv.reader((x.replace('\0', '') for x in f), delimiter = ',')
    for row in csv_reader:
        documents.append(remove2Char(removeSpecialChar(removeStopWords(removeURLs(row[1])))))

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]

dictionary = corpora.Dictionary(texts)
dictionary.save('deerwester.dict')  # store the dictionary, for future reference

#Corpus Created
corpus = [dictionary.doc2bow(text) for text in texts]

print("Corpus Created")
path_to_dtm_binary = "/home/khan/DTM/dtm/dtm/main"

model = DtmModel(path_to_dtm_binary,
corpus, time_slices=[1] * len(corpus),
mode='fit', model='dtm', num_topics=20)

print("Model fitted")
topics = model.show_topic(topicid=1, time=1, topn=10)
print(topics)
print("Topics finding")
training_time = time.time() - start_time

# Coverting topic into a excel file
print("Putting in DataFrame started")
df = pd.DataFrame(topics)
writer = pd.ExcelWriter("DTM_topics.xlsx")
df.to_excel(writer, 'Sheet1')

df1 = pd.DataFrame([training_time])
df1.to_excel(writer, 'Sheet2')
writer.save()
