"""
    @author Suhas Vittal
    Script for GAN using tensorflow
"""

import tensorflow as tf
import numpy as np
import keras
from keras import backend as K
from sklearn.preprocessing import normalize
import scipy.stats

import matplotlib.pyplot as plt

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

def develop_gan(num_inputs, hidden_layers=[[5], [5]], noise_size=100,
            dropout=0.4):
    # create generator
    G = keras.models.Sequential()

    for i in range(len(hidden_layers[0])):
        if i == 0:
            G.add(keras.layers.Dense(hidden_layers[0][i], input_shape=(noise_size,),
                    activation=tf.nn.relu))
        else:
            G.add(keras.layers.Dense(hidden_layers[0][i], activation=tf.nn.relu))
    G.add(keras.layers.Dense(num_inputs, activation=tf.nn.sigmoid))
    # create discriminator
    D = keras.models.Sequential()

    for i in range(len(hidden_layers[1])):
        if i == 0:
            D.add(keras.layers.Dense(hidden_layers[1][i], input_shape=(num_inputs,),
                    activation=tf.nn.leaky_relu))
        else:
            D.add(keras.layers.Dense(hidden_layers[1][i], activation=tf.nn.leaky_relu))

    D.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

    return G, D

def train(gan, training_sets, alpha=0.01, beta=0.9, decay=6e-8,
            train_iter=1000, batch_size=50, noise_size=100):
    # create discriminative and adversarial models

    G, D = gan

    DM = keras.models.Sequential()
    DM.add(D)
    d_opt = keras.optimizers.SGD(lr=alpha, momentum=beta, decay=decay)
    #d_opt = keras.optimizers.RMSprop(lr=alpha, decay=decay)
    DM.compile(loss="binary_crossentropy", optimizer=d_opt,
            metrics=["accuracy"])

    AM = keras.models.Sequential()
    AM.add(G)
    AM.add(D)
    a_opt = keras.optimizers.SGD(lr=alpha/2.0, momentum=beta, decay=decay/2.0)
    #a_opt = keras.optimizers.RMSprop(lr=alpha/2.0, decay=decay/2.0)
    AM.compile(loss="binary_crossentropy", optimizer=a_opt,
            metrics=["accuracy"])

    DL = [[],[]]
    AL = [[],[]]

    for k in range(train_iter):
        x_train = training_sets[np.random.randint(0, high=training_sets.shape[0],
                    size=batch_size)]
        noise = np.random.uniform(-1.0, 1.0, [batch_size, noise_size])
        x_fake = G.predict(noise)
        x = np.concatenate((x_train, x_fake))
        y = np.ones([2*batch_size, 1])
        y[batch_size:, :] = 0
        d_loss = DM.train_on_batch(x, y)

        y = np.ones([batch_size, 1])
        noise = np.random.uniform(-1.0, 1.0, size=[batch_size, noise_size])
        a_loss = AM.train_on_batch(noise, y)
        log_msg = "%d: [D loss: %f, acc: %f]" % (k, d_loss[0], d_loss[1])
        log_msg = "%s [A loss: %f, acc: %f]" % (log_msg, a_loss[0], a_loss[1])

        DL[0].append(d_loss[0])
        DL[1].append(d_loss[1])
        AL[0].append(a_loss[0])
        AL[1].append(a_loss[1])

        if k % 25 == 0:
            print(log_msg)

        # early stopping: DL = ln 4
        if d_loss[0] > 1.5 or a_loss[0] == 0.0:
            break

    plt.plot(DL[0])
    plt.plot(AL[0])
    plt.show()
    plt.plot(DL[1])
    plt.plot(AL[1])
    plt.show()

    return G, D

def extract_samples(G, size=100, noise_size=100):
    noise = np.random.uniform(-1.0, 1.0, size=[size, noise_size])
    samps = G.predict(noise)
    return samps
