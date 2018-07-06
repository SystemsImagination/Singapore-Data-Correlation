#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 10:59:48 2018

@author: Suhas Vittal
"""

import numpy as np
import scipy.stats.mstats as sp

LEARNING_RATE = 0.001
MOMENTUM_RATE = 0.1
EPS = 0.000001

X = []
class MLP:
    # class for a multilayer perceptron
    # activation is tanh.
    
    def __init__(self, num_inputs, num_outputs, num_hl=1, 
                 num_hlnodes=10, af=np.tanh, regularization=0.0):
        self.N = num_inputs
        self.M = num_outputs
        self.HL = num_hl
        self.HLN = num_hlnodes
        self.activation = af
        self.lambd = regularization
        
        weights = []
        for i in range(num_hl + 1):
            if i == 0:
                W = 2*np.random.rand(num_hlnodes, num_inputs)-1.0
                #W = np.zeros((num_hlnodes, num_inputs))
            elif i == num_hl:
                W = 2*np.random.rand(num_outputs, num_hlnodes)-1.0
                #W = np.zeros((num_outputs, num_hlnodes))
            else:
                W = 2*np.random.rand(num_hlnodes, num_hlnodes)-1.0
                #W = np.zeros((num_hlnodes, num_hlnodes))
            weights.append(W)
        self.weights = weights
        
    
    def predict(self, inputs):
        # predicts output based on input

        X = np.asarray(inputs)
        A = X
        
        for W in self.weights:
            A = self.activation(W.dot(A))
        
        return A

    def train(self, training_sets, actual, epochs=10, use_softmax=False):
        softmax = lambda z: np.exp(z) / (np.sum(np.exp(z)))
        # softmax should be true if using multinomial classifier.
        
        # trains the MLP on the training sets
        # training_sets is a list of x_vectors
        # actual is a list of y-vectors
        
        prev_err = None
        err = 0.0
        
        prev_delta = 0.0
        
        momentums = []
        first_mom_update = True
        for e in range(epochs):
            print("Epoch: " + str(e))
            D = []
            
            print(self.weights[0][0][0])
            
            for k in range(len(actual)):
                if k % 100==0:
                    print("\tTraining set: " + str(k))
                y = np.asarray([actual[k]]).transpose()
                x = np.asarray([training_sets[k]]).transpose()
                A = []
                a = x
                
                for i in range(len(self.weights)):
                    W = self.weights[i]
                    A.append(a)
                    if i == len(self.weights)-1 and use_softmax:
                        a = softmax(W.dot(a))
                    else:
                        a = self.activation(W.dot(a))
                # do not append last a, because that is prediction.
                error = []
                
                for i in range(self.HL+1):
                    j = -i
                    
                    if i == 0:
                        E = y - a
                        err += E
                        error.append(E)
                    else:
                        W = self.weights[j]
                        a = A[j]
                        E = W.transpose().dot(error[-1]) * (a * (1 - a))
                        error.append(E)
                        
                if not D:
                    for i in range(len(A)):
                        D.append(error[-(i+1)].dot(A[i].transpose()))
                else:
                    for i in range(len(A)):
                        D[i] = D[i] + error[-(i+1)].dot(A[i].transpose())
            
            for i in range(len(D)):
                d = D[i]
                W = self.weights[i]
                m = float(len(actual))
                
                if first_mom_update:
                    dW = -LEARNING_RATE*((1.0/m)*d + self.lambd*W)
                    momentums.append(dW)
                else:
                    dW = momentums[i]
                    dW = MOMENTUM_RATE*dW -LEARNING_RATE*((1.0/m)*d + self.lambd*W)
                    momentums[i] = dW
                W = W + LEARNING_RATE*((1.0/m)*d + self.lambd*W) - MOMENTUM_RATE*dW
                self.weights[i] = W
            
            err = np.log(np.abs(err) / (len(actual)+0.1))
            print("\tError norm: " + str(np.linalg.norm(err)))
            
            if not first_mom_update:
                print("\tPrev. Error norm: " + str(np.linalg.norm(
                        prev_err
                    )))
                delta = np.linalg.norm(err - prev_err)
                
                print("\tChange in DELTA: " + str(delta-prev_delta))
                if np.abs(delta-prev_delta) < EPS and e > 20:
                    break
                
                prev_delta = delta
            prev_err = err
            err = 0.0
            
            first_mom_update = False
        print("Finished learning.")

def make_discrete(vector, NA_as_zero=True):
    label_dict = {}
    new_vector = []
    k = 0 # next new key
    
    if NA_as_zero:
        label_dict["NA"] = 0
        k += 1
    
    for y in vector:
        if y not in label_dict.keys():
            label_dict[y] = k
            new_vector.append(k)
            k += 1
        else:
            new_vector.append(label_dict[y])
    
    return new_vector, label_dict

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
    actual = []
    line = reader.readline()
    while line != "":
        data = line.split(",")
        
        explanatory = [0.0 if x=="?" or x=="NA" else float(x) for x in data[33:137]]

        #response = data[192:210]
        #response = [data[212], data[214], data[216], data[217]]
        response=data[235:265]
        
        if not explanatory or not response:
            line = reader.readline()
            continue
    
        training_sets.append(explanatory)
        actual.append(response)
        line = reader.readline()
    print("finished reading.")
    
    d_res = []
    print(actual)
    for i in range(len(actual[0])):
        col = []
        for j in range(len(actual)):
            col.append(actual[j][i])
        temp, label_dict = make_discrete(col)
        print("Response variable\t|" + str(i))
        for item in label_dict.items():
            k, v = item
            print("\t" + str(k) + "\t:\t" + str(v))
        d_res.append(temp)
        
    # want to get transpose of d_res
    temp = []
    for i in range(len(d_res[0])):
        row = []
        for j in range(len(d_res)):
            row.append(d_res[j][i])
        temp.append(row)
    d_res = temp
    actual = d_res
    
    def polylog(z, n=3):
        w = z
        for _ in range(n):
            w = np.log(np.abs(w))
        return w
    def sigmoid(z):
        return 1.0 / (1.0 + np.exp(-z))
    def softmax(z):
        return np.exp(z) / np.sum(np.exp(z))
    def softplus(z):
        return np.log(1.0+np.exp(z))
    
    def TBR(z): # tight bounds rectifier
        w = np.ndarray(z.shape)
        shape = z.shape
        
        F = lambda x: np.tanh(softplus(x))
        
        if len(shape) == 1:
            for i in range(len(z)):
                w[i] = F(z[i])
        else:
            for i in range(len(z)):
                for j in range(len(z[i])):
                    w[i, j] = F(z[i, j])
        return w
    
    
    training_sets = rank_normalize(training_sets)
    print(training_sets)
    
    MLP = MLP(len(training_sets[0]), len(actual[0]), num_hl=200, 
              num_hlnodes=75, 
              af=TBR, 
              regularization=0.5)

    MLP.train(training_sets, actual, epochs=2000, use_softmax=True)
    # save weights and output data
    for i in range(len(MLP.weights)):
        W = MLP.weights[i]
        np.save("TBR_3/W_" + str(i) + ".npy", W)
    
    for i in range(len(training_sets)):
        p = MLP.predict(training_sets[i])
        
        writer = open("TBR_3/results/output_TS-" + str(i) + ".tsv", "w+")
        writer.write("var_num\tP-A\tGOOD?")
        num_good = 0
        for j in range(len(p)):
            diff = p[j] - actual[i][j]
            good = "GOOD" if np.abs(diff) < 0.5 else "BAD"
            if good == "GOOD":
                num_good += 1
            writer.write("\n" + str(j) + "\t" + str(diff) + "\t" + good)
        
        writer.write("\n\n" + str(num_good) + "\t" + str(len(p) - num_good))
        writer.close()