# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:59:15 2018

@author: groot
"""

import numpy as np
import re

# This script aims to discretize labels amongst phenotypes.
# The algorithm is as follows. For a list L of phenotypes, we
# go through each label in L. We find the following statistics:
#   mean
#   minimum
#   maximum
# From this, we can make 4 classes. Let LM = (mean+min)/2 and UM = (mean+max)/2:
#   0: min -> LM
#   1: LM -> M
#   2: M -> UM
#   3: UM -> M

# Above is the standard algorithm. We can generalize the number of classes to 
# some EVEN number N by finding exactly (N/2)-1 classes btwn an extremum and
# the mean.

def discretize(column, N=4):
    # column is a vector. Please represent as some array type.
    # N is the number of classes, and is an EVEN non-negative integer.
    
    label = column[0] # the label.
    dcol = [label] # the discrete column; the output.
    
    k = 1
    
    minimum = -1
    maximum = -1
    mean = 0
    
    while k < len(column):
        dp = column[k]
        
        if minimum < 0 or minimum > dp:
            minimum = dp
        elif maximum > 0 or maximum < dp:
            maximum = dp
            
        mean = (mean*(k-1) + dp)/k
        
        k += 1
    
    X = (N/2)-1 # number of classes between an extremum and the mean.
    
    # first check if a value V > mean. If so, z = floor(V / (mean+max))
    # if z > X, then within ((n-1)X -> max)
    
    for val in column:
        if val > mean:
            z = np.floor(val / ((mean+maximum)/X))
            cl = z + (X+1)
            dcol.append(cl)
        else:
            z = np.floor(val / ((mean + minimum)/X))
            cl = z
            dcol.append(cl)
    
    return dcol

if __name__ == "__main__":
    N = 6 # number of classes. Please adjust as necessary.
    
    # We will discriminate phenotypes from other datatypes using regex.
    # Currently, this discriminates against:
    #   miRNA
    file = "phen-miRNA.csv"
    
    reader = open(file, "r")
    writer = open("phen-miRNA_discrete.csv", "w+")
    
    lines = reader.readlines()
    dataset = [lines[0]]
    dataset.extend([[float(x) for x in line.split(",")] for line in lines[1:]])
    
    # for each column, we would like to make the edit.
    new_lines = ["" for _ in len(dataset)]
    for i in range(len(dataset[0])):
        new_col = discretize(dataset[:,i], N=N)
        
        for j in len(new_col):
            if i == 0:
                new_lines[j] += str(new_col[j])
            else:
                new_lines[j] += "," + str(new_col[j])
    
    first = True
    for line in new_lines:
        if first:
            first = False
            writer.write(line)
        else:
            writer.write("\n" + line)
            
    reader.close()
    writer.close()
            
    