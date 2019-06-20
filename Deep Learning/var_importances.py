#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 15:43:14 2018

@author: Suhas Vittal
"""

# This script computes variable importances of weights in a given
# folder.

import numpy as np

W_EXT = "W_"
folder = "TBR_2"

def compute_importance(std_dev, w, was_rank_normalized=True):
    if was_rank_normalized:
        return (sum([np.abs(x) for x in w]))
    else:
        return (std_dev) * (sum([np.abs(x) for x in w]))

if __name__ == "__main__":
    reader = open("cohort_whatisnormal_MODDED.csv", "r")
    header = reader.readline().split(",")[33:137]
    
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
    
    # need to compute the std_dev
    training_sets = np.asarray(training_sets)
    std_dev = [np.std(training_sets[:, i]) for i in range(len(training_sets[0]))]
    
    W = np.load(folder + "/" + W_EXT + "0.npy") # first weight matrix
    
    imp = []
    for i in range(len(header)):
        I = compute_importance(std_dev[i], W[:, i])
        imp.append(I)
    
    # get median of imp
    med = np.median(imp)
    mean = np.sum(imp) / len(imp)
    print("Mean: " + str(mean))
    for i in range(len(header)):
        if imp[i] > mean:
            print(str(i) + "|\t" + header[i] + "\t:\t" + str(imp[i]))