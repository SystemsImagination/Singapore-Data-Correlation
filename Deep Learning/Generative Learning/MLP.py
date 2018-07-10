#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 10:59:48 2018

@author: Suhas Vittal
"""

import numpy as np
import scipy.stats.mstats as sp
from activations import *
from adjustments import *

X = []
class LogisticMLP:
    # class for a multilayer perceptron
    # activation is tanh.

    def __init__(self, num_inputs, num_outputs, num_hl=1,
                 num_hlnodes=10, af=tanh, regularization=0.0, use_biases=False):
        self.N = num_inputs
        self.M = num_outputs
        self.HL = num_hl
        self.HLN = num_hlnodes
        self.activation = af
        self.lambd = regularization

        weights = []
        for i in range(num_hl + 1):
            if i == 0:
                W = (2*np.random.rand(num_hlnodes, num_inputs))*0.01
                #W = np.zeros((num_hlnodes, num_inputs))
            elif i == num_hl:
                W = (2*np.random.rand(num_outputs, num_hlnodes))*0.01
                #W = np.zeros((num_outputs, num_hlnodes))
            else:
                W = (2*np.random.rand(num_hlnodes, num_hlnodes))*0.01
                #W = np.zeros((num_hlnodes, num_hlnodes))
            weights.append(W)
        self.weights = weights

        self.use_biases = use_biases
        if use_biases:
            biases = []
            for i in range(num_hl + 1):
                if i == num_hl:
                    b = (2*np.random.rand(num_outputs,1))*0.01
                else:
                    b = (2*np.random.rand(num_hlnodes,1))*0.01
                biases.append(b)
            self.biases = biases

    def predict(self, inputs):
        # predicts output based on input

        x = np.asarray(inputs)
        a = x
        for i in range(len(self.weights)):
            W = self.weights[i]
            if self.use_biases:
                b = self.biases[i]
            else:
                b = 0.0

            a = self.activation(W.dot(a) + b)
        return a

    def stoc_train(self, training_sets, actual, epochs=10,
            alpha=0.1, beta=0.1, EPS=0.01):
        # trains the MLP on the training sets
        # training_sets is a list of x_vectors
        # actual is a list of y-vectors

        # alpha is LEARNING_RATE
        # beta is MOMENTUM_RATE

        momentums = []
        prev_J = 0
        J = 0
        first_mom_update = True
        for e in range(epochs):
            print("Epoch: " + str(e))

            for k in range(len(actual)):
                y = np.asarray([actual[k]]).transpose()
                x = np.asarray([training_sets[k]]).transpose()
                A = []
                a = x

                for i in range(len(self.weights)):
                    W = self.weights[i]
                    A.append(a)

                    if self.use_biases:
                        b = self.biases[i]
                    else:
                        b = 0.0

                    a = self.activation(W.dot(a) + b)

                # do not append last a, because that is prediction.
                error = []
                j = 0.0
                max_class = np.max(y) # get the maximal class in a
                for c in range(max_class+1):
                    bin_col = [[1.0] if y[i][0]==c else [0.0] for i in range(y.shape[0])]
                    bin_col = np.asarray(bin_col) # make col vector
                    j += bin_col.transpose().dot(np.log(a))
                J = j # update objective

                for i in range(self.HL+1):
                    j = -i
                    if i == 0:
                        E = a-y
                        error.append(E)
                    else:
                        W = self.weights[j]
                        a = A[j]
                        E = W.transpose().dot(error[-1]) * (a * (1 - a))
                        error.append(E)

                for i in range(len(self.weights)):
                    W = self.weights[i]
                    wd = error[-(i+1)].dot(A[i].transpose())

                    if first_mom_update:
                        dW = -alpha*(wd + self.lambd*W)
                        momentums.append(dW)
                    else:
                        dW = beta*momentums[i] - alpha*(wd + self.lambd*W)
                        momentums[i] = dW
                    W = W - alpha*(wd + self.lambd*W) + beta*dW
                    self.weights[i] = W

                    if self.use_biases==True:
                        bd = error[-(i+1)]
                        b = self.biases[i]
                        b = b - alpha*bd
                        self.biases[i] = b

                if not first_mom_update and k % 100 == 0:
                    print("\tObjective: " + str(J))
                    print("\tChange in Objective: " + str(J-prev_J))
                    if np.abs(J-prev_J) < EPS and e > epochs*0.01:
                        print("Finished Learning")
                        return
                first_mom_update = False
                prev_J = J
        print("Finished learning.")

    def batch_train(self, training_sets, actual, epochs=10,
            alpha=0.1, beta=0.1, EPS=0.01):
        # softmax should be true if using multinomial classifier.

        # trains the MLP on the training sets
        # training_sets is a list of x_vectors
        # actual is a list of y-vectors

        # alpha is LEARNING_RATE
        # beta is MOMENTUM_RATE

        momentums = []
        prev_J = 0
        first_mom_update = True
        for e in range(epochs):
            print("Epoch: " + str(e))
            wD = [] # deltas for weights
            bD = [] # deltas for biases

            J = 0
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

                    if self.use_biases:
                        b = self.biases[i]
                    else:
                        b = 0.0

                    a = self.activation(W.dot(a) + b)

                # do not append last a, because that is prediction.
                error = []
                j = 0.0
                max_class = np.max(y) # get the maximal class in a
                for c in range(max_class):
                    bin_col = [[1.0] if y[i][0]==c else [0.0] for i in range(y.shape[0])]
                    bin_col = np.asarray(bin_col) # make col vector
                    j += bin_col.transpose().dot(np.log(a))
                J += j # update objective


                for i in range(self.HL+1):
                    j = -i

                    if i == 0:
                        E = a-y
                        error.append(E)
                    else:
                        W = self.weights[j]
                        a = A[j]
                        E = W.transpose().dot(error[-1]) * (a * (1 - a))
                        error.append(E)

                if not wD:
                    for i in range(len(A)):
                        wD.append(error[-(i+1)].dot(A[i].transpose()))
                        bD.append(error[-(i+1)])
                else:
                    for i in range(len(A)):
                        wD[i] = wD[i] + error[-(i+1)].dot(A[i].transpose())
                        bD[i] = bD[i] + error[-(i+1)]

            for i in range(len(wD)):
                wd = wD[i]
                W = self.weights[i]
                m = float(len(actual))

                if first_mom_update:
                    dW = -alpha*((1.0/m)*wd + self.lambd*W)
                    momentums.append(dW)
                else:
                    dW = momentums[i]
                    dW = beta*dW -alpha*((1.0/m)*wd + self.lambd*W)
                    momentums[i] = dW
                W = W - alpha*((1.0/m)*wd + self.lambd*W) + beta*dW
                self.weights[i] = W

                if self.use_biases:
                    # update biases using deltas
                    bd = bD[i]
                    b = self.biases[i]
                    b = b - alpha*((1.0 / m)*bd)
                    self.biases[i] = b

            J = J / len(actual)
            if not first_mom_update:
                print("\tObjective: " + str(J))
                print("\tChange in Objective: " + str(J-prev_J))
                if np.abs(J-prev_J) < EPS:
                    break

            prev_J = J
            first_mom_update = False
        print("Finished learning.")

if __name__ == "__main__":
    reader = open("cohort_whatisnormal_MODDED.csv", "r")
    header = reader.readline().split(",")

    training_sets = []
    actual = []
    line = reader.readline()
    while line != "":
        data = line.split(",")

        explanatory = [0.0 if x=="?" or x=="NA" else float(x) for x in data[33:137]]

        response = data[192:210]
        #response = [data[212], data[214], data[216], data[217]]
        #response=data[235:265]

        if not explanatory or not response:
            line = reader.readline()
            continue

        training_sets.append(explanatory)
        actual.append(response)
        line = reader.readline()
    print("finished reading.")

    d_res = []
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


    training_sets = standardize(rank_normalize(training_sets))

    MLP = LogisticMLP(len(training_sets[0]), len(actual[0]), num_hl=200,
              num_hlnodes=75,
              af=softmax,
              regularization=0.5, use_biases=True)

    MLP.stoc_train(training_sets, actual, epochs=2000, alpha=0.01, beta=0.01)
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
