#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 12:19:06 2018

@author: Suhas Vittal
"""

# This is a script to run Independent Components Analysis (ICA)
# to test for independence.

import numpy as np
from sklearn.preprocessing import normalize

LEARNING_RATE = 0.01
MOMENTUM_RATE = 0.1
density_f = np.tanh
F = lambda z: np.exp(-z) / (1.0 + np.exp(-z))

def ICA(training_sets, num_iter=1000):
    X = training_sets # the noisy samples
    # We seek to find an "unmixing" matrix W such that XW = S
    # where S is the non-noisy samples of each variable.
    
    # If a variable is truly independent, then S_i = X_i.
    m = len(X)
    n = len(X[0])
    W = np.random.rand(n, n)
    dW = [[None]] # momentum
    
    X = np.asarray(X)
    X = normalize(X, axis=1, norm="l1")
    
    prev_LOGLOSS = None
    
    for e in range(num_iter):
        print("Iteration: " + str(e))
        
        # get LOGLOSS
        LOGLOSS = 0.0
        for i in range(m):
            for j in range(n):
                w = W[j].transpose()
                x = X[i].transpose()
                LOGLOSS += np.log(F(w.dot(x))) + np.log(np.linalg.det(W))
        LOGLOSS = LOGLOSS * (1/m)
        
        print("\tLOGLOSS: " + str(LOGLOSS))
        if prev_LOGLOSS == None:
            prev_LOGLOSS = LOGLOSS
        else:
            dLL =LOGLOSS - prev_LOGLOSS
            print("\tChange in LOGLOSS: " + str(dLL))
            prev_LOGLOSS = LOGLOSS
            
            if dLL < 0.1:
                break
        
        for x in X:
            x = np.asarray([x]).transpose() # make col vector
            cdf_M = []
            for w in W:
                # for each row vector
                cdf_M.append(1.0 - 2*density_f(w.transpose().dot(x)[0]))
            cdf_M = np.asarray([cdf_M]).transpose()
            
            grad = cdf_M.dot(x.transpose()) + np.linalg.inv(W.transpose())
            if dW[0][0] == None:
                dW = LEARNING_RATE * grad
            else:
                dW = MOMENTUM_RATE * dW + LEARNING_RATE * grad
            
            W = W + LEARNING_RATE * grad + MOMENTUM_RATE * dW
    return X.dot(W) # return original signals

def rank_normalize(training_sets):
    new_ts = training_sets
    new_ts = np.asarray(new_ts)
    for i in range(new_ts.shape[1]):
        # for each col
        sorted_col = np.sort(new_ts[:, i])
        rank_dict = {sorted_col[i] : i for i in range(len(sorted_col))}
        for j in range(new_ts.shape[0]):
            new_ts[j][i] = rank_dict[new_ts[j][i]]
    
    return new_ts

if __name__ == "__main__":
    reader = open("cohort_whatisnormal_MODDED.csv", "r")
    header = reader.readline().split(",") 
    
    training_sets = []
    line = reader.readline()
    while line != "":
        data = line.split(",")
        
        explanatory = [0.0 if x=="?" or x=="NA" else float(x) for x in data[33:137]]
        
        if not explanatory:
            line = reader.readline()
            continue
    
        training_sets.append(explanatory)
        line = reader.readline()
    print("finished reading.")
    
    # normalize training data
    training_sets = np.asarray(training_sets)
    training_sets = normalize(training_sets, axis=1, norm="l1")
    
    S = ICA(training_sets, num_iter=1000).transpose()
    print("Original:\n\t" + str(training_sets[0]))
    print("New:\n\t" + str(S[0]))