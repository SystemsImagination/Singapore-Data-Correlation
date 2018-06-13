# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 11:52:34 2018

@author: Suhas Vittal
"""

# This script aims to place a non-linear fit on phenotype-lipid relationships,
# using an SVM.

import numpy as np
import re
from sklearn import svm

response = "Gender"

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
    
    Y = dataset[:vc_index, i] # get the i-th column as the response var
    X = dataset[:vc_index, 289:] # get the lipid columns as the explanatory var
    
    clf = svm.SVC(kernel="poly")
    clf.fit(X, Y)
    
    val_Y = dataset[vc_index:, i]
    val_X = dataset[vc_index:, 289:]
    
    score = clf.score(val_X, val_Y)
    
    print("Score of non-linear SVM on validation data was: " + str(score))