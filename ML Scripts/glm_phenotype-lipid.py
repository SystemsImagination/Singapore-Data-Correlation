# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:17:56 2018

@author: Suhas Vittal
"""

# This script runs a generalized linear model (binary classification scheme currently) 
# on phenotype vs lipid concentrations.

# Please write the input file below:

input_file = "phen-lipids_discrete.csv"

import re
import h2o
from h2o.estimators import H2OGeneralizedLinearEstimator

if __name__ == "__main__":

    h2o.init() # initialize the local host
    h2o_df = h2o.import_file(input_file)
    
    # For ease of access, we would like to read the response and explanatory variables from the
    # input file and place them in an array. Fortunately for us, this is a simple
    # regex match ;)
    
    reader = open(input_file, "r")
    header_line = reader.readline().split(",")
    reader.close()
    
    res_var = []
    exp_var = []
    
    k = 0
    for label in header_line:
        if k > 288:
            exp_var.append(label.strip())
        elif not (label == "iOmicsno" or label == "sample-id" or label == "CASPro-rAP" or label == "RT" or re.match("(E)+(per)*", label)):
            res_var.append(label.strip())
        else:
            pass
        k += 1
    
    # Back to the ML.   
          
    optimal_r2 = 0.50
    conn_exists = []
    dont_even = []
        
    for response in res_var: 
        h2o_df[response] = h2o_df[response].asfactor() # declare response as discrete.
        model = H2OGeneralizedLinearEstimator(family="binomial", model_id="py_glm-" + response)
        
        r = h2o_df.runif(seed=1234)
        ts = h2o_df[r < 0.8] # the training set
        vs = h2o_df[r >= 0.8] # the validation set
        
        model.train(y=response, x=exp_var, training_frame=ts, validation_frame=vs)
        
        print(model.r2(valid=True))
        r2 = model.r2(valid=True)
        
        if r2 != "-Infinity" and r2 > optimal_r2:
            conn_exists.append(response)
        elif r2 != "-Infinity" and r2 < 0:
            dont_even.append((response, r2))
    
    print("These appear to be significant.")
    for r in conn_exists:
        print("\t" + str(r))
    
    print("\nDon't even try fitting these.")
    for r in dont_even:
        res, r2 = r
        print("\t" + str(res) + "\tr2 = " + str(r2))