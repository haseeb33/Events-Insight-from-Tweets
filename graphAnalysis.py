#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 15:21:32 2019

@author: khan
"""

import pandas as pd
import matplotlib.pyplot as plt

tweet_values = []

f = pd.ExcelFile("1000_topics_morethan3tweets_#.xlsx")
topics_df = pd.read_excel(f, sheet_name = "Sheet1")
print("Topics loaded")
theta_df = pd.read_excel(f, sheet_name = "Sheet2")
print("Theta Values loaded")
frequency_df = pd.read_excel(f, sheet_name = "Sheet3")
print("Frequency of tweets also loaded")

#Converting to list variables
topics_ls = topics_df.values.tolist()
theta_ls = theta_df.values.tolist()
frequency_ls = frequency_df.values.tolist()

# Estimated tweets based on theta and frequency of tweets values
estimated_tweets = []
all_tweets_one_day = {}
for idx, val in enumerate(frequency_ls):
    temp = [j * val[1] for j in theta_ls[idx]]
    estimated_tweets.append(temp)
    tag = val[0].split("_")
    date = str(tag[-3]) + "/" + str(tag[-2])
    if date in all_tweets_one_day.keys():
        all_tweets_one_day[date] = [x + y for x, y in zip(temp, all_tweets_one_day[date])]
    else:
        all_tweets_one_day[date] = temp

#Checking the top tweets
total = []
for i in range(1000):
    count = 0
    for j in all_tweets_one_day.keys():
        count += all_tweets_one_day[j][i]
    total.append(count)

new_l = sorted(enumerate(total), key=lambda x:-x[1])

#Graph Plotting3
sorted_date = sorted(all_tweets_one_day.keys())

def graph(topic):
    est_tweet = []
    for j in sorted_date:
        est_tweet.append(all_tweets_one_day[j][topic])
    plt.plot(sorted_date, est_tweet)
    tweet_values.append(est_tweet[2:])
    plt.grid()
    plt.show()

    print("Top words in this topic:")
    print(topics_ls[topic])

    top_tags = top_hashtags(topic)
    top_tags_ls = []
    for idx, tag in enumerate(top_tags[:20]):
        a = frequency_ls[tag[0]]
        b = round(tag[1], 2)
        c = round(tag[1]/frequency_ls[tag[0]][1], 3)
        top_tags_ls.append([a,b,c])
    print("Top hashtags for this topic:")
    print(sorted(top_tags_ls, key=lambda x: x[2], reverse = True))

def top_hashtags(topic):
    unordered = []
    for idx, theta in enumerate(theta_ls):
        unordered.append(frequency_ls[idx][1] * theta[topic])

    top_topics = sorted(enumerate(unordered), key=lambda x:-x[1])
    return(top_topics)

def show_all_graphs(start = 0, end = 1000):
    for i in range(start, end):
        wewe = input("Press e to exit/other key to continue = ")
        if wewe == 'e':
            break
        else:
            print(str(i) + "th topic's graph")
            graph(i)

def top_topics(hashtag):
    position = None
    for idx, val in enumerate(frequency_ls):
        if val[0] == hashtag:
            position = idx
            break
    tag = [frequency_ls[position][1] * x for x in theta_ls[position]]
    or_tag = sorted(enumerate(tag), key=lambda x:-x[1])
    return(or_tag)

#sorted({k:sum(v) for k, v in all_tweets_one_day.items()}.items(), key=lambda x:x[0]) Total number of tweets per day
