#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 14:42:49 2018

@author: Suhas Vittal
"""

import numpy as np

# This script is an implementation of Restricted
# Boltzmann Machines.

def train_RBM(training_sets):
    num_visible = len(training_sets[0])
    num_hidden = len(training_sets[0])/2 + 1
    
    A = np.asarray([0.0 for _ in range(num_visible)]) # visible bias
    B = np.asarray([0.0 for _ in range(num_hidden)]) # hidden bias
    
    W = np.random.rand(num_visible, num_hidden)
    
    def E(v, h):
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
    
        
        
    
    for v from training_sets:
        

