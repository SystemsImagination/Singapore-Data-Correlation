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

"""
    Best results so far (meaning with most accurate models):
        DG(18 1_20 3)
        PC(33 3)
        HexCer(d18 1 18 0)
        SM(32 0)
        TG(16 1_17 0_18 1)
        PC(16 0_22 6)
        PI(36 4)
        PC(28 0)
        PC(40 7)
        PC(O-38 4)
        PC(32 0)
        PE(O-40 6)
        TG(14 1_16 0_18 1)
        LPE(18 0)
        Cer(d18 1 20 0)
        TG(14 1_16 1_18 0)
        PC(35 2)
        PC(37 5)
        SM(37 2)
        SM(34 3)
        CE(18 0)
        CE(22 5)
        DG(18 2_20 3)
"""

import h2o
from h2o.estimators import H2ODeepLearningEstimator

file = "phen-lipids_discrete.csv"
LOS = (1.00 + 0.75) / 2.0 # Above the average


if __name__ == "__main__":
    h2o.init() # initialize localhost
    
    global_impor = set()
    
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
                                         activation="Rectifier", 
                                         hidden=[num_hlnodes],
                                         loss="CrossEntropy")
        model.train(x=exp_var, y=res, training_frame=ts, validation_frame=vs)
        
        variables = model._model_json["output"]["variable_importances"]["variable"]
        vimpor = model._model_json["output"]["variable_importances"]["scaled_importance"]
        
        print("Coefficient of Determination for Response " + str(res) + ": " + str(model.r2()))
        
        most_impor = []
        for i in range(len(variables)):
            im = vimpor[i] # get variable importance
            if im > LOS: 
                var = variables[i]
                most_impor.append(var)
        
        if not global_impor:
            # if the set is empty.
            global_impor = set(most_impor)
        else:
            # take the intersection
            global_impor = global_impor.intersection(set(most_impor))
    
    print("\n\nImportant Variables amongst the labels " + ", ".join(res_vars) + " are:")
    for var in global_impor:
        print("\t" + str(var))
    
    