import numpy as np
from gan import *
from sklearn.preprocessing import normalize
import scipy.stats

import matplotlib.pyplot as plt

if __name__ == "__main__":
    # create GAN
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

    training_sets = np.asarray(training_sets)
    training_sets = normalize(training_sets)

    HL = [200 for _ in range(10)]

    gan = develop_gan(len(explanatory), hidden_layers=[HL, HL])
    G, D = train(gan, training_sets, alpha=2e-3, train_iter=100000, batch_size=205)

    print("finished training.")
    # get some samples
    samples = np.asarray(extract_samples(G, size=100))
    """
        after ensuring that the model returns good samples, we now want to examine
        sets of standard deviations to determine whether or not
        certain proteins are independent.

        This is naive treatment of data as independent proteins can have wildly
        different variances, but considering that the alternative is a O(2^n)
        operation (meaning we would have to do 2^500 calculations), doing simple
        500 is a better option. Also, the rationale is that the expression of
        certain proteins may or may not induce/repress the expression of others.
    """

    """
        conduct Kruskal-Wallis test
    """
    mean_H = 0.0
    mean_P = 0.0
    for i in range(training_sets.shape[1]):
        ts_col = training_sets[:, i]
        sp_col = samples[:, i]

        H, p = scipy.stats.kruskal(ts_col, sp_col)
        mean_H += H
        mean_P += p
    mean_H = mean_H / training_sets.shape[1]
    mean_P = mean_P / training_sets.shape[1]
    print(mean_H, mean_P)

    writer = open("gan_scores.tsv", "w+")
    writer.write("\t".join(header[33:137]))

    for _ in range(100):
        std_dev = {i:[] for i in range(training_sets.shape[1])}
        num_iter = 10
        for _ in range(num_iter):
            samps = np.asarray(extract_samples(G, size=100))
            for i in range(samps.shape[1]):
                sd = np.std(samps[:, i])
                std_dev[i].append(sd)
        populations = []
        for arr in std_dev.values():
            populations.append(arr)
        populations = np.asarray(populations)

        scores = 0.0
        for i in range(populations.shape[1]):
            w = populations[:, i]
            mean = np.mean(w)
            scores += w - mean
        scores = (scores / np.min(np.abs(scores))) / (len(scores))
        # write the scores to the file
        score_ln = "\n" + "\t".join([str(x) for x in scores])
        writer.write(score_ln)
    writer.close()
