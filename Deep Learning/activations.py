#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 11:43:54 2018

@author: Suhas Vittal
"""
import numpy as np

# implementations of commonly used activation functions

def maxout(z):
    max_array = []
    for i in range(z.shape[0]):
        row = z[i]
        # we want the max element in the row
        max_array.append(np.max(row))
    max_array = np.asarray([max_array]).transpose()
    return max_array

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def softmax(z):
    return np.exp(z) / np.sum(np.exp(z))

def leaky_relu(z):
    for i in range(z.shape[1]):
        u = z[0][i]
        if u >= 0:
            z[0][i] = u
        else:
            z[0][i] = 0.01*u
    return z

def tanh(z):
    return (1.0 + np.tanh(z)) / 2.0
