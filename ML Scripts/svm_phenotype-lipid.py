# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 11:52:34 2018

@author: Suhas Vittal
"""

# This script aims to place a non-linear fit on phenotype-lipid relationships,
# using an SVM.

import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn import svm
import seaborn as sns

response = "BMI"

if __name__ == "__main__":
    reader = open("phen-lipids_discrete.csv", "r")
    lines = [line.split(",") for line in reader.readlines()]
    
    reader.close()
    
    # construct float dataset
    dataset = []
    
    for row in lines[1:]:
        dataset.append([float(x.strip()) if x != "NA" and not re.match("M.*", x) and x.strip() != "" else 0.0 for x in row[1:]])
    
    dataset = np.asarray(dataset)
    
    res_index = 0 # we need to find the index for the response variable
    for i in range(len(lines[0])):
        header = lines[0][i]
        
        if header == response:
            res_index = i - 1 # we removed the first column
            break
    
    validation_cutoff = 0.8 # percent of data to use for training data
    vc_index = int(np.ceil(dataset.shape[0] * 0.8))
    
    Y = dataset[:vc_index, res_index] # get the i-th column as the response var
    X = dataset[:vc_index, 289:] # get the lipid columns as the explanatory var
    
    clf = svm.SVC(kernel="linear")
    clf.fit(X, Y)
    
    val_Y = dataset[vc_index:, res_index]
    val_X = dataset[vc_index:, 289:]
    
    score = clf.score(val_X, val_Y) # Accuracy score. Higher is better.
    
    print("Score of SVM on validation data was: " + str(score))
    
    coef = clf.coef_[0]
    
    # we want data that beats a = 0.01. We make a distribution.
    mean = sum(coef) / float(len(coef))
    stdev = 0
    
    for c in coef:
        stdev += (c - mean)**2
        
    stdev = np.sqrt(stdev / float(len(coef)))
    
    critval = 2.807 # critical value for 99.5% (as LOS = 0.01) confidence interval.
    
    # we want data outside 3*stdev
    L = mean - 1.5*stdev
    U = mean + 1.5*stdev
    
    print(L, U)
    
    writer = open("SVM/Lipid-" + lines[0][res_index+1] + ".tsv", "w+")
    
    writer.write("Lipid\tClass\tCoefficient")
    for i in range(len(coef)):
        lipid = lines[0][289 + i]

        if coef[i] < L:
            writer.write("\n" + lipid + "\t0\t" + str(coef[i]))
        if coef[i] > U:
            writer.write("\n" + lipid + "\t1\t" + str(coef[i]))
            
    writer.close()
    
    sorted_coef = sorted(coef)
    bins = int(np.floor(len(sorted_coef) / 5.0))
    sns.distplot(sorted_coef, hist=True, kde=True, bins=bins, color = 'darkblue', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 4})
    
    
    
    