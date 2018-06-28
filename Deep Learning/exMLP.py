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

# Script for experimental MLPs. (deep learning)

DELTAS = []
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
                W = (2*np.random.rand(num_hlnodes, num_inputs)-1.0)/(num_hl+1)
                #W = np.zeros((num_hlnodes, num_inputs))
            elif i == num_hl:
                W = (2*np.random.rand(num_outputs, num_hlnodes)-1.0)/(num_hl+1)
                #W = np.zeros((num_outputs, num_hlnodes))
            else:
                W = (2*np.random.rand(num_hlnodes, num_hlnodes)-1.0)/(num_hl+1)
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

    def train(self, training_sets, actual, epochs=10):
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
                
                for W in self.weights:
                    A.append(a)
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
                        d_af = (self.activation(a+0.001) - 
                                self.activation(a-0.001)) / (2*0.001)
                        E = W.transpose().dot(error[-1]) * d_af
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
                DELTAS.append(np.abs(delta-prev_delta))
                if np.abs(delta-prev_delta) < EPS and e > 20:
                    break
                
                prev_delta = delta
            prev_err = err
            err = 0.0
            
            first_mom_update = False
        print("Finished learning.")

if __name__ == "__main__":
    reader = open("cohort.csv", "r")
    header = reader.readline().split(",") 
    
    training_sets = []
    actual = []
    line = reader.readline()
    while line != "":
        data = line.split(",")
        
        explanatory = [0.0 if x=="?" else float(x) for x in data[2:115]]


        response = [1 if x == "Yes" else 0 for x in data[115:304]]
        if not explanatory or not response:
            line = reader.readline()
            continue
    
        training_sets.append(explanatory)
        actual.append(response)
        line = reader.readline()
    print("finished reading.")
    
    def polylog(z, n=3):
        w = z
        for _ in range(n):
            w = np.log(np.abs(w))
        return w
    def sigmoid(z):
        return 1.0 / (1.0 + np.exp(-z))
    def softplus(z):
        return np.log(1.0+np.exp(z))

    def TBR(z): # tight bounds rectifier (idk i just made it up)
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
    
    MLP = MLP(len(training_sets[0]), len(actual[0]), num_hl=20, 
              num_hlnodes=75, 
              af=TBR, 
              regularization=0.5)

    MLP.train(training_sets, actual, epochs=2000)
    
    # save MLP data to CSV
    for i in range(len(MLP.weights)):
        W = MLP.weights[i]
        np.save("TBR/W_" + str(i) + ".npy", W)
    
    for i in range(len(training_sets)):
        p = MLP.predict(training_sets[i])
        
        writer = open("TBR/results/output_TS-" + str(i) + ".tsv", "w+")
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
    