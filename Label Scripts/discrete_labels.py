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
# From this, we can make 4 classes. Let LM = min+(mean-min)/2 and UM = mean+(mean-max)/2:
#   0: min -> LM
#   1: LM -> M
#   2: M -> UM
#   3: UM -> M

# Above is the standard algorithm. We can generalize the number of classes to 
# some EVEN number N by finding exactly (N/2)-1 classes btwn an extremum and
# the mean.

# NOTE THAT THE DISCRETE CLASSES ARE NOT UNIFORM AND ARE AFFECTED BY SPREAD.

def discretize(column, N=4):
    # column is a vector. Please represent as some array type.
    # N is the number of classes, and is an EVEN non-negative integer.
    
    # returns new column, and statistics used to create column.
    # Format: (col, min, mean, max, X)
    
    label = column[0] # the label.
    dcol = [] # the discrete column; the output.
    
    k = 1
    
    minimum = -1
    maximum = -1
    mean = 0
    
    print("\tcolumn name: " + str(column[0]))
    while k < len(column):
        #print("\tComponent No.: " + str(k))
        
        dp = column[k]
        if is_number_regex(dp):
            dp = float(dp)
        else:
            k += 1
            continue
        
        if minimum == -1 or minimum > dp:
            minimum = dp
        elif maximum == -1 or maximum < dp:
            maximum = dp
            
        mean = (mean*(k-1) + dp)/k
        
        k += 1
    
    X = (N/2)-1 # number of classes between an extremum and the mean.
    
    print("\tmean: " + str(mean))
    print("\tmin: " + str(minimum))
    print("\tmax: " + str(maximum))
    
    # first check if a value V > mean. If so, z = floor(V / (mean-max))
    # if z > X, then within ((n-1)X -> max)
    
    for val in column:
        if is_number_regex(val):
            val = float(val)
        else:
            dcol.append(val)
            continue
        
        if mean == 0 and minimum == 0 and maximum == 0:
            dcol.append(0)
        elif val > mean:
            z = np.floor((val-mean) / ((maximum-mean)/X))
            if z > X:
                z = X
            cl = z + (X+1)
            dcol.append(cl)
        else:
            z = np.floor((val-minimum) / ((mean-minimum)/X))
            if z < 0:
                z = 0
            cl = z
            dcol.append(cl)
    
    return (dcol, minimum, mean, maximum, X)

def is_number_regex(s):
    """ Returns True is string is a number. """
    if re.match("^\d+?\.\d+?$", s) is None:
        return s.isdigit()
    return True

def get_col(matrix, i):
    # gets i-th column of given matrix
    
    col = []
    for j in range(len(matrix)):
        col.append(matrix[j][i])
    
    return col

if __name__ == "__main__":
    N = 6 # number of classes. Please adjust as necessary.
    
    # We will discriminate phenotypes from other datatypes using regex.
    # Currently, this discriminates against:
    #   miRNA
    file = "phen-miRNA.csv"
    
    reader = open(file, "r")
    dwriter = open("phen-miRNA_discrete.csv", "w+")
    iwriter = open("phen-miRNA_discrete-info.csv", "w+")
    
    lines = [line.split(",") for line in reader.readlines()]
    dataset = []
    
    first = True
    upp_bnd = 0
    for line in lines:
        nl = []
        if first:
            first = False
            for i in range(len(line)):
                if re.match("hsa", line[i]):
                    upp_bnd = i
                    break
                else:
                    nl.append(line[i])
        else:
            for i in range(upp_bnd):
                nl.append(line[i])
        dataset.append(nl)
                    
    
    
    # for each column, we would like to make the edit.
    
    #print(dataset)
    iwriter.write("Column Name" + ",".join([str(i) for i in range(N)]))
    
    new_lines = ["" for _ in range(len(dataset))]
    for i in range(len(dataset[0])):
        print("column: " + str(i))
        new_col, m, mean, M, X = discretize(get_col(dataset, i), N=N)
        
        X = int(X)
        info_line = "\n" + str(new_col[0]) + ","# get name
        classes = [m + n*(mean - m)/X for n in range(X)] # makeclasses
        classes.extend([mean + n*(M-mean)/X for n in range(X)]) 
        classes.append(M)
        
        info_line += ",".join(["\"" + str(classes[i]) + "-->" + str(classes[i+1]) + "\"" for i in range(len(classes)-1)])
        iwriter.write(info_line)
        
        
        print(len(dataset),len(new_col))
        for j in range(len(new_col)):
            if i == 0:
                new_lines[j] += str(new_col[j])
            else:
                new_lines[j] += "," + str(new_col[j])
    
    first = True
    for line in new_lines:
        if first:
            first = False
            dwriter.write(line)
        else:
            dwriter.write("\n" + line)
            
    reader.close()
    dwriter.close()
    iwriter.close()
            
    