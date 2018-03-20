#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 14:04:28 2018

@author: vikasshenoy
"""
import numpy as np
import csv
import random
import os
import xlrd as xlrd
import modifiedthirdpartycode as file
#from untitled12 import apriori, generateRules

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
#movement=c

(m,n) = movement.shape

sym = np.empty([10,n], dtype="<U100")

for i in range(10):
    for j in range(n):
            if(movement[i][j]==0):
                if symbols[i] in dicti:
                    sym[i][j]=dicti[symbols[i]]+symbols[i]+'_DOWN'
                else:
                    sym[i][j]="NO_SEC"+symbols[i]+'_DOWN'
            else:
                if symbols[i] in dicti:
                    sym[i][j]=dicti[symbols[i]]+symbols[i]+'_UP'
                else:
                    sym[i][j]="NO_SEC"+symbols[i]+'_UP'

sym=np.transpose(sym)

lsym=sym.tolist()

l1,support_data1=file.apriori(lsym)
interest=['MMM','AES']
part='dependent'
file.generateRules(l1, support_data1, interest, part)

    

                