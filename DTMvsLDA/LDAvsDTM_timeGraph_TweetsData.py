#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 17:03:59 2019

@author: khan
"""
import matplotlib.pyplot as plt
from math import log

x = [3, 3.5, 4, 4.5, 5, 5.5] # Log of no of docs

dtm20 = [42.86, 190.88, 592.80, 1844.69, 5663.21, 21480.49]
dtm20log = [log(x, 10) for x in dtm20]
dtm50 = [79.68, 340.38, 1116.42, 3531.24, 10801.09, 42781.83]
dtm50log = [log(x, 10) for x in dtm50]
dtm100 = [129.79, 590.29, 1967.31, 5987.03, 18436.17, 74270.23]
dtm100log = [log(x, 10) for x in dtm100]

lda20 = [4.92, 10.98, 15.56, 30.30, 64.55, 151.74]
lda20log = [log(x, 10) for x in lda20]
lda50 = [7.71, 17.82, 31.74, 60.10, 124.75, 291.90]
lda50log = [log(x, 10) for x in lda50]
lda100 = [13.71, 30.97, 51.05, 105.87, 220.42, 536.41]
lda100log = [log(x, 10) for x in lda100]


def log_graph():
    plt.plot(x, dtm20log, 'g--', label = "20 Topics DTM")
    plt.plot(x, lda20log, 'r--', label = "20 Topics LDA")

    plt.plot(x, dtm50log, 'g-.', label = "50 Topics DTM")
    plt.plot(x, lda50log, 'r-.', label = "50 Topics LDA")

    plt.plot(x, dtm100log, 'g:', label = "100 Topics DTM")
    plt.plot(x, lda100log, 'r:', label = "100 Topics LDA")
    
    plt.xlabel("Log(Number of Docs)")
    plt.ylabel("Log(Training Time(Sec))")
    plt.legend(loc = "best")
    plt.show()
    
def normal_graph():
    plt.plot(x, dtm20, 'g--', label = "20 Topics DTM")
    plt.plot(x, lda20, 'r--', label = "20 Topics LDA")

    plt.plot(x, dtm50, 'g-.', label = "50 Topics DTM")
    plt.plot(x, lda50, 'r-.', label = "50 Topics LDA")

    plt.plot(x, dtm100, 'g:', label = "100 Topics DTM")
    plt.plot(x, lda100, 'r:', label = "100 Topics LDA")
    
    plt.xlabel("Log(Number of Docs)")
    plt.ylabel("Training Time(Sec)")
    plt.legend(loc = "best")
    plt.show()