#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 20:12:10 2018

@author: vikasshenoy
"""
############################################
# K-means based Clustering for Stock Prices#
############################################

import numpy as np
import csv
import random
import os
import numpy.random 

def dist(a, b, ax=1):
    return np.linalg.norm(a - b, axis=ax)

def km(X, K, max_iters):
    (m,n)=X.shape
    C=np.random.rand(K,n)
    clusters = np.zeros(len(X))

    for p in range(max_iters):
        for i in range(len(X)):
            distances = dist(X[i], C)
            cluster = np.argmin(distances)
            clusters[i] = cluster
        for i in range(K):
            points = [X[j] for j in range(len(X)) if clusters[j] == i]
            C[i] = np.mean(points, axis=0)
    
    return clusters

with open(r"/Users/vikasshenoy/Desktop/Financial Data Mining/assignment_07(1)/stocks/sp500_short_period.csv") as csvfile:
    csvData = csv.reader(csvfile)
    datList = []
    for row in csvData:
        datList.append(row)

symbols = np.array(datList.pop(0))

data = np.array(datList)
data = data.astype(np.float)
c = np.double((data[1:np.size(data, 0), :] - data[0:np.size(data, 0) - 1, :]) > 0)
movement = np.transpose(c)

K = 10                          # 10 sectors so that 10 classes
max_iters = 1000                # maximum iterations
random.seed(1234)
idx = km(movement, K, max_iters)

for k in range(K):
    print('\nStocks in group %d moving up together\n' % (k+1))
    k = np.array(k)
    index = np.squeeze(idx == k)
    print(symbols[np.where(index)])