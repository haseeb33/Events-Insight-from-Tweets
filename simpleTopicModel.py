#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 19:52:23 2018

@author: khan
"""

import pytm
import csv

only_text = []
with open('english_tweets.txt', mode = 'r') as f:
    csv_reader = csv.reader(f, delimiter = ',')
    for row in csv_reader:
        only_text.append(row[1])
    f.close()

with open('only_tweets.txt', mode = 'w') as f:
    csv_writer = csv.writer(f, delimiter = ',')
    for row in only_text:
        csv_writer.writerow(row)
    f.close()

docs = pytm.DocumentSet(open('only_tweets.txt').readline(),min_df=5, max_df=0.5)

n_topics = 100
lda = pytm.SVILDA(n_topics, docs.get_n_vocab())
lda.fit(docs, 100)

alphas = [lda.get_alpha(k) for k in range(n_topics)]
for k, alpha in enumerate(alphas):
    vocab = docs.get_vocab()
    phi = lda.get_phi(k)
    print('topic {0} (alpha = {1})'.format(k, alpha))
    print(sorted(zip(vocab, phi), key=lambda x: -x[1])[:10])
