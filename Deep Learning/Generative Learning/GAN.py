#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 13:40:50 2018

@author: Suhas Vittal

Script to run GAN, as detailed in
Goodfellow et al. 2014 "Generative Adversarial Nets".

Will plan to include other types of GANs, such as
the WGAN.
"""

from MLP import LogisticMLP
from activations import *
from adjustments import *

import numpy as np

PRED_DIFF = 0.001

class GAN:
    # Has two MLPs. A generator and a discriminator.

    def __init__(self, num_features, num_hl=50, num_hlnodes=75,
                 af=[maxout, maxout], use_biases=True, K=1):
        # K is a hyperparameter that determines how much the
        # discriminator is trained per epoch

        self.gen = LogisticMLP(num_features, num_features, num_hl=num_hl,
                       num_hlnodes=num_hlnodes, af=af[0],
                       use_biases=use_biases)
        self.dis = LogisticMLP(num_features, 1, num_hl=num_hl,
                       num_hlnodes=num_hlnodes, af=af[1],
                       use_biases=use_biases)
        self.K = K
        self.use_biases = use_biases

    def batch_train(self, training_set, samp_step=50, prior=None, epochs=100, alpha=0.1, beta=0.1):
        # train on the features

        if prior==None:
            prior = lambda n: np.random.normal(0.0, 1.0, size=(n, training_set.shape[1]))

        training_set = np.asarray(training_set)

        mom_g = []
        for e in range(epochs):
            print("Epoch: " + str(e))

            first_momG_update = True
            print("On Discriminator")
            for _ in range(self.K):
                wDdis = []
                bDdis = []
                J = 0.0

                z_samps = prior(samp_step)
                x_samps = [training_set[np.random.randint(0, high=len(training_set))] for _ in range(samp_step)]
                first_momD_update = True
                mom_d = []

                for i in range(len(x_samps)):
                    x = np.asarray([x_samps[i]]).transpose()
                    z = np.asarray([z_samps[i]]).transpose()
                    A = []
                    a = x

                    for j in range(len(self.dis.weights)):
                        W = self.dis.weights[j]
                        A.append(a)

                        if self.use_biases:
                            b = self.dis.biases[j]
                        else:
                            b = 0.0

                        if i == len(self.dis.weights)-1:
                            a = W.dot(a) + b
                        else:
                            a = self.dis.activation(W.dot(a) + b)

                    # training step
                    # calculate J for this example
                    J += np.log(a) + (1 - np.log(
                            self.d_predict(self.g_predict(z))
                        ))
                    error = []

                    for j in range(self.dis.HL+1):
                        if j == 0:
                            E = 0.5-a
                        else:
                            W = self.dis.weights[-j]
                            c = A[-j]
                            E = W.transpose().dot(error[-1]) * (c * (1-c))
                        error.append(E)

                    if not wDdis:
                        for j in range(len(A)):

                            wDdis.append(
                                    error[-(j+1)].dot(A[j].transpose())
                            )
                            bDdis.append(
                                    error[-(j+1)]
                            )
                    else:
                        for j in range(len(A)):
                            wDdis[j] = wDdis[j] + error[-(j+1)].dot(A[j].transpose())
                            bDdis[j] = bDdis[j] + error[-(j+1)]
                for i in range(len(self.dis.weights)):
                    wd = wDdis[i]
                    W = self.dis.weights[i]
                    m = samp_step

                    if first_momD_update:
                        p = alpha*(1/m)*wd
                        mom_d.append(p)
                    else:
                        p = beta*mom_d[i] + alpha*(1/m)*wd
                        mom_d[i] = p

                    W = W + alpha*(1/m)*wd + beta*p
                    self.dis.weights[i] = W

                    if self.use_biases:
                        b = self.dis.biases[i]
                        bd = bDdis[i]
                        b = b + alpha*(1/m)*bd
                        self.dis.biases[i] = b
                first_momD_update = False
                print("Discriminator Objective: " + str(J))
            rn = np.random.randint(0, high=z_samps.shape[0])
            # get random number from 0 --> m.
            samp = np.asarray([z_samps[rn]]).transpose() # rand training set
            pred_dis = self.d_predict(self.g_predict(samp))

            print("Discriminator predicts: " + str(pred_dis[0]))
            if 0.5-PRED_DIFF < pred_dis[0] < 0.5+PRED_DIFF and e > epochs * 0.1:
                break
            # according to Goodfellow et al. 2014, D = 0.5 indicates
            # that the generator is making very good FAUX sets as the
            # discriminator is being forced to "guess" whether or not
            # a training example is real. This is what we want.

            print("On Generator")
            wDgen = []
            bDgen = []

            z_samps = prior(samp_step)

            for i in range(len(z_samps)):
                z = np.asarray([z_samps[i]]).transpose()

                A = []
                a = z

                for j in range(len(self.gen.weights)):
                    W = self.gen.weights[j]
                    A.append(a)
                    if self.use_biases:
                        b = self.gen.biases[j]
                    else:
                        b = 0.0

                    if i == len(self.gen.weights)-1:
                        a = W.dot(a) + b
                    else:
                        a = self.gen.activation(W.dot(a) + b)
                error = []

                for j in range(self.gen.HL+1):
                    if j == 0:
                        E = 0-a
                    else:
                        W = self.gen.weights[-j]
                        c = A[-j]
                        E = W.transpose().dot(error[-1]) * (c * (1-c))
                    error.append(E)

                if not wDgen:
                    for j in range(len(A)):
                        wDgen.append(
                                error[-(j+1)].dot(A[j].transpose())
                        )
                        bDgen.append(
                                error[-(j+1)]
                        )
                else:
                    for j in range(len(A)):
                        wDgen[j] = wDgen[j] + error[-(j+1)].dot(A[j].transpose())
                        bDgen[j] = bDgen[j] + error[-(j+1)]
            for  i in range(len(wDgen)):
                wd = wDgen[i]
                W = self.gen.weights[i]
                m = samp_step

                if first_momG_update:
                    p = -alpha*(1/m)*wd
                    mom_g.append(p)
                else:
                    p = beta*mom_g[i] - alpha*(1/m)*wd
                    mom_g[i] = p


                W = W - alpha*(1/m)*wd + beta*p
                self.gen.weights[i] = W

                if self.use_biases:
                    b = self.gen.biases[i]
                    bd = bDgen[i]
                    b = b - alpha*(1/m)*bd
                    self.gen.biases[i] = b
            first_momG_update=False
        print("Done")

        z_samps = prior(samp_step)
        gen_guess = self.g_predict(z_samps[3])
        return gen_guess

    def d_predict(self, inputs):
        # predicts output based on input

        x = np.asarray(inputs)
        a = x
        for i in range(len(self.dis.weights)):
            W = self.dis.weights[i]
            if self.use_biases:
                b = self.dis.biases[i]
            else:
                b = 0.0

            if i == len(self.dis.weights)-1:
                a = W.dot(a) + b
            else:
                a = self.dis.activation(W.dot(a) + b)

        return a

    def g_predict(self, inputs):
        # predicts output based on input

        x = np.asarray(inputs)
        a = x
        for i in range(len(self.gen.weights)):
            W = self.gen.weights[i]
            if self.use_biases:
                b = self.gen.biases[i]
            else:
                b = 0.0
            if i == len(self.gen.weights)-1:
                a = W.dot(a) + b
            else:
                a = self.gen.activation(W.dot(a) + b)
        return a

if __name__ == "__main__":
    reader = open("cohort_whatisnormal_MODDED.csv", "r")
    header = reader.readline().split(",")

    training_sets = []
    actual = []
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


    gan = GAN(num_features=len(explanatory),
              num_hl=35, num_hlnodes=25, af=[maxout, maxout],
              use_biases=True)

    training_sets, max_vals = standardize(training_sets)
    training_sets = np.asarray(training_sets)
    max_vals = np.asarray(max_vals)

    prior_mean = []
    for i in range(training_sets.shape[1]):
        m = np.mean(training_sets[:, i])
        prior_mean.append(m)
    prior_cov = np.cov(training_sets, rowvar=False, bias=True)
    prior = lambda n: np.random.multivariate_normal(prior_mean, prior_cov, size=n)

    prior_sp = lambda n: np.random.normal(0, 10, size=(n, training_sets.shape[1]))
    prior_rn = lambda n: np.random.rand(n, training_sets.shape[1])

    gen_guess = gan.batch_train(training_sets, prior=prior_sp, epochs=2000, alpha=0.01, beta=0.01)
    gen_guess = max_vals * gen_guess
    print(gen_guess)
    print(max_vals*training_sets[3])
