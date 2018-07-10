"""
    @author Suhas Vittal

    Script contains data adjustment procedures such as:
        standardization
        rank normalization
"""

import numpy as np

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

def standardize(training_sets):
    new_ts = training_sets
    new_ts = np.asarray(new_ts)

    max_vals = []
    for i in range(new_ts.shape[1]):
        # get maximal element
        M = np.max(new_ts[:, i])
        max_vals.append(M)
        new_col = new_ts[:, i] / M
        new_ts[:, i] = new_col

    return new_ts, max_vals
