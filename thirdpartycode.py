#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 14:29:04 2018

@author: vikasshenoy
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xlrd as xlrd
#-*- coding:utf-8 - *-
def createC1(dataset):
    "Create a list of candidate item sets of size one."
    c1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    #print(c1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    #frozenset because it will be a ket of a dictionary.
    return map(frozenset, c1)


def scanD(dataset, candidates, min_support,num_items):
    "Returns all candidates that meets a minimum support level"
    sscnt = {}
    for tid in dataset:
        for can in candidates:
            if can.issubset(tid):
                sscnt.setdefault(can, 0)
                sscnt[can] += 1
    #num_items = float(len(dataset))
    retlist = []
    support_data = {}
    for key in sscnt:
        support = sscnt[key] / num_items
     
        if support >= min_support:
            retlist.insert(0, key)
        support_data[key] = support
    return retlist, support_data


def aprioriGen(freq_sets, k):
    "Generate the joint transactions from candidate sets"
    retList = []
    lenLk = len(freq_sets)
    #print(lenLk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(freq_sets[i])[:k - 2]
            L2 = list(freq_sets[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(freq_sets[i] | freq_sets[j])
    return retList


def apriori(dataset, minsupport=0.00002):
    "Generate a list of candidate item sets"
    C1 = createC1(dataset)
    D = list(map(set,dataset))
    num_items = float(len(dataset))
    L1, support_data = scanD(D, C1, minsupport,num_items)
    L = [L1]
    #print(L[0])
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minsupport,num_items)
        support_data.update(supK)
        L.append(Lk)
        k += 1

    return L, support_data

def generateRules(L, support_data, interest, part='antecedent', min_confidence=0.6):
    """Create the association rules
    L: list of frequent item sets
    support_data: support data for those itemsets
    min_confidence: minimum confidence threshold
    """
    rules = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rules_from_conseq(freqSet, H1, support_data, rules, interest, part, min_confidence)
            else:
                calc_confidence(freqSet, H1, support_data, rules, interest, part, min_confidence)
    return rules


def calc_confidence(freqSet, H, support_data, rules, interest, part='antecedent', min_confidence=0.6):
    "Evaluate the rule generated"
    pruned_H = []
    for conseq in H:
        conf = support_data[freqSet] / support_data[freqSet - conseq]
        if conf >= min_confidence:
            for var in interest:
                if((var+'_DOWN' in (freqSet - conseq)) or (var+'_UP' in (freqSet - conseq))):
                    #print(freqSet - conseq)
                    print (freqSet - conseq, '--->', conseq, 'conf:', conf)
                    rules.append((freqSet - conseq, conseq, conf))
                    pruned_H.append(conseq)
    return pruned_H


def rules_from_conseq(freqSet, H, support_data, rules, interest, part='antecedent', min_confidence=0.6):
    "Generate a set of candidate rules"
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calc_confidence(freqSet, Hmp1,  support_data, rules,  interest, part, min_confidence)
        if len(Hmp1) > 1:
            rules_from_conseq(freqSet, Hmp1, support_data, rules, interest, part, min_confidence)
            
def load_dataset():
    dict = {}
    wb = xlrd.open_workbook('/Users/vikasshenoy/Desktop/Financial Data Mining/assignment_07(1)/foodmart/product.xlsx', 'r')
    sh = wb.sheet_by_index(0)   
    for i in range(1560):
        cell_value_class = sh.cell(i,1).value
        cell_value_id = sh.cell(i,3).value
        dict[cell_value_class] = cell_value_id
    data = []
    with open('/Users/vikasshenoy/Desktop/Financial Data Mining/assignment_07(1)/foodmart/basket.dat', 'r') as f:
        d = f.readlines()
        for i in d:
            k = i.rstrip().split(",")
            data.append([dict[int(i)] for i in k])
    return data