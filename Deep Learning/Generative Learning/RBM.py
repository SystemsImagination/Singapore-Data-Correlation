#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 14:42:49 2018

@author: Suhas Vittal
"""

import numpy as np

# This script is an implementation of Restricted
# Boltzmann Machines.

RATE = 0.01

def train_RBM(training_sets):
    # input is the set of training sets.
    # output is the weight matrix, visible biases, and hidden biases.
    
    num_visible = len(training_sets[0])
    num_hidden = len(training_sets[0])/2 + 1
    
    A = np.asarray([0.0 for _ in range(num_visible)]) # visible bias
    B = np.asarray([0.0 for _ in range(num_hidden)]) # hidden bias
    
    W = np.random.rand(num_visible, num_hidden)
    
    def E(v, h): # the energy function
        _v = np.asarray(v)
        _h = np.asarray(h)
        
        return -1.0 * (A.transpose().dot(_v) 
                       + B.transpose().dot(_h) +
                       _v.transpose().dot(W.dot(h)))
        
        
    def pdf():
        # v and h are vectors of visible and hidden units.
        
        Z = 0.0
        for _v in training_sets:
            Z += np.exp(-E(_v, h))
        return (1.0 / Z) * np.exp(-E(v, h))
    
    def sig(z): # sigmoid function
        return 1.0 / (1.0 + np.exp(-z))
    
    def prob_h(v): # returns the probability of each h given v
        prob_h = []
        
        for j in range(len(B)):
            val = B[j]
            for i in range(len(v)):
                val += W[i][j] * v[i]
            prob_h.append(sig(val))
        return np.asarray(prob_h)
    
    def prob_v(h): # returns the probability of each v given h
        prob_v = []
        
        for i in range(len(A)):
            val = A[i]
            for j in range(len(h)):
                val += W[i][j] * h[j]
            prob_v.append(sig(val))
        return np.asarray(prob_v)
    
    for v in training_sets:
        prob_h = prob_h(v)
        h = np.asarray([np.random.binomial(1, prob_h[i]) for i in range(len(prob_h))])
        # the sampled hidden vector from the prob_h distribution.
        
        Gpos = v.dot(h.transpose()) # outer product.
        
        prob_vpr = prob_v(h)
        vpr = np.asarray([np.random.binomial(1, prob_vpr[i]) for i in range(len(prob_vpr))])
        prob_hpr = prob_h(vpr)
        hpr = np.asarray([np.random.binomial(1, prob_hpr[i]) for i in range(len(prob_hpr))])
        # two reconstructed vectors
        
        Gneg = vpr.dot(hpr.transpose()) # outer product again
        
        dW = RATE * (Gpos - Gneg)
        dA = RATE * (v - vpr)
        dB = RATE * (h - hpr)
        
        W = W - dW
        A = A - dA
        B = B - dB
    
    return W, A, B

def compute_importance(w, std_dev):
    return std_dev * sum([np.abs(x) for x in w])

if __name__ == "__main__":
    
