# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 12:49:08 2018

@author: Suhas Vittal
"""

# This script uses a neural network to predict phenotypes from a set of lipids.
# Unlike the SVM, this script uses the h2o documentation like the GLM script.

# The setup will be a feedfoward ANN that backpropogates with SGD. We will use
# the sigmoid (hyperbolic tangent) function for each of the function nodes, and
# have a hidden layer of 5 nodes as there are 5 lipid classes, documented in
# lipid_classifier.py.

# We are viewing connections between:
res_vars = ["Gender", "BMI", "GLU_1", "CHO_1", "TG_1", "HDL_1", "CHDL_1", "LDLM_1", "HbA1c_1", "A1_1"]

import h2o
import numpy as np
from h2o.estimators import H2ODeepLearningEstimator

file = "phen-lipids_discrete.csv"


if __name__ == "__main__":
    h2o.init() # initialize localhost
    
    global_impor = set()
    used_res = []
    
    for res in res_vars:
        h2o_df = h2o.import_file(file)
        h2o_df[res] = h2o_df[res].asfactor() # make response variable
        # discrete.
        
        exp_var = []
        reader = open(file, "r")
        header_line = reader.readline().split(",")
        reader.close()
        
        k = 0
        for label in header_line:
            if k > 288:
                exp_var.append(label.strip())
            k += 1
        
        r = h2o_df.runif(seed=1234)
        ts = h2o_df[r < 0.8] # training set
        vs = h2o_df[r >= 0.8] # validation set
        
        num_hlnodes = int((len(exp_var) + 2) / 2)
        
        model = H2ODeepLearningEstimator(model_id="ann_Lipid-" + res, 
                                         distribution="bernoulli", 
                                         activation="TanhWithDropout", 
                                         hidden=[num_hlnodes, 25, num_hlnodes],
                                         loss="CrossEntropy",
                                         epochs=5)
                                         
        model.train(x=exp_var, y=res, training_frame=ts, validation_frame=vs)
        
        variables = model._model_json["output"]["variable_importances"]["variable"]
        vimpor = model._model_json["output"]["variable_importances"]["scaled_importance"]
        r2 = model.r2(valid=True)
        
        print("Coefficient of Determination for Response " + str(res) + ": " + str(r2))
        
        if r2 > 0.5: # we want okay data. Even 0.5 is stretching it.
            used_res.append(res)
            
            mean = 0
            for im in vimpor:
                mean += im
            mean = mean / float(len(vimpor))
            
            stdev = 0
            for x in vimpor:
                stdev += (x - mean)**2
            stdev = np.sqrt(stdev / float(len(vimpor)))
            
            critval = 2.807 # for 95% confidnece
            
            U_CI = mean + critval * stdev / np.sqrt(len(vimpor))
            
            most_impor = []
            for i in range(len(variables)):
                im = vimpor[i] # get variable importance
                if im > U_CI: 
                    var = variables[i]
                    most_impor.append(var)
            
            if not global_impor:
                # if the set is empty.
                global_impor = set(most_impor)
            else:
                # take the intersection
                global_impor = global_impor.intersection(set(most_impor))
    
    print("\n\nImportant Variables amongst the labels " + ", ".join(used_res) + " are:")
    for var in global_impor:
        print("\t" + str(var))
    
    