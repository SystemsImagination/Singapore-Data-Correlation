# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 10:50:33 2018

@author: Suhas Vittal
"""
# This script aims to place a non-linear fit on lipid-miRNA relationships,
# using an SVM.

import numpy as np
import re
from sklearn import svm

response = "Cer(d18 0 20 0)"

if __name__ == "__main__":
    reader = open("lipids-miRNA.tsv", "r")
    lines = [line.split("\t") for line in reader.readlines()]
    
    reader.close()
    
    # construct float dataset
    dataset = []
    
    for row in lines[1:]:
        dataset.append([float(x.strip()) if x != "NA" and not re.match("M.*", x) and x.strip() != "" else 0.0 for x in row[1:]])
    
    dataset = np.asarray(dataset)
    
    res_index = 0 # we need to find the index for the response variable
    hsa_col = 0
    for i in range(len(lines[0])):
        header = lines[0][i]
        
        if header == response:
            res_index = i
        if re.match("hsa", header):
            hsa_col = i
            break
    
    validation_cutoff = 0.8 # percent of data to use for training data
    vc_index = int(np.ceil(dataset.shape[0] * validation_cutoff))
    
    Y = dataset[:vc_index, res_index] # get the i-th column as the response var
    X = dataset[:vc_index, hsa_col:] # get the lipid columns as the explanatory var
    
    clf = svm.SVR(kernel="poly", degree=1)
    clf.fit(X, Y)
    
    val_Y = dataset[vc_index:, res_index]
    val_X = dataset[vc_index:, hsa_col:]
    
    score = clf.score(val_X, val_Y) # Accuracy score. Higher is better.
    
    print("Determination score of SVM on validation data was: " + str(score))
    
    # we are interested in the coefficients, though. 
    
    # Note that the assays fo miRNAs measure how difficult it is to activate a
    # given miRNA. Noting that miRNAs are a specific type of snRNA (small nuclear
    # RNA) and often inhibit the translation of miRNAs, miRNA and lipid relations
    # are important to see as an operon may express a catalyst for a given lipid
    # in one of its genes, but an miRNA may be inhibiting the translation of the
    # gene's corresponding RNA transcript. Given this information, a coefficient
    # that is greater than or equal to (1 + K), where K is some constant of confidence,
    # would indicate that an miRNA has no relationship as an miRNA with a low
    # activation threshold and a lipid with a high concentration would logically have
    # no relationship: the lipid's catalyst is not prevented from being created
    # by the miRNA. 
    
    # To this end, we will list miRNA's with coefficients >= (1 + K).
    K = 1.5 # arbitrary boundary.
    """
    coef = clf.coef_[0]
    
    # we want data that beats a = 0.01. We make a distribution.
    mean = sum(coef) / float(len(coef))
    stdev = 0
    
    for c in coef:
        stdev += (c - mean)**2
        
    stdev = np.sqrt(stdev / float(len(coef)))
    
    critval = 1.96 # critical value for 99.5% (as LOS = 0.01) confidence interval.
    
    # we want data outside the following confidence interval
    dM = critval * (stdev / np.sqrt(len(coef)))
    L_CI = mean - dM
    U_CI = mean + dM
    
    print(L_CI, U_CI)
    
    writer = open("miRNA-" + lines[0][res_index] + ".tsv", "w+")
    
    writer.write("miRNA\tRelation\tCoefficient")
    for i in range(len(coef)):
        miRNA = lines[0][hsa_col + i] # get the miRNA header
        
        if coef[i] < L_CI:
            print("Important adverse miRNA: " + str(miRNA) + "\twith coefficient: " + str(coef[i]))
        if coef[i] > U_CI:
            print("Important non-interfering miRNA: " + str(miRNA) + "\twith coefficient: " + str(coef[i]))
        writer.write("\n" + str(miRNA) + "\tadverse\t" + str(coef[i]))
    """
    
