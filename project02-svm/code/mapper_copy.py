#!/usr/bin/env python2.7

import sys

import numpy as np


m = 50
dims = 400
mean = np.zeros(dims);
cov = np.zeros((dims, dims))
np.fill_diagonal(cov, 1)

pi_times_2 = np.pi * 2
sqrt2 = np.sqrt(2)




# DEBUG: read from file in argument instead of stdin
if len(sys.argv) > 1:
    sys.stdin = open(sys.argv[1], 'r')


# This function has to either stay in this form or implement the
# feature mapping. For details refer to the handout pdf.
def transform(x_original):
    # omega = np.random.multivariate_normal(mean, cov, size=m)
    # b = np.random.uniform(0, pi_times_2, size=m)
    # dotProd = np.dot(omega, x_original)
    # retval = sqrt2 * np.cos(dotProd + b)
    # retval /= np.sqrt(m)
    # return retval
    return x_original


#Parameter x: list of ndarray
#Parameter y: list of classifications
#Parameter k: corresponds to |A_t|
def process_junk(x_arr, y_arr, k, _lambda, w, t):
    if len(x_arr) == 0:
        # we have no misclassification for this junk
        return w

    zipped = zip(x_arr, y_arr)
    res = sum([tu[0] * tu[1] for tu in zipped]) / k

    # gradient
    gradient_vec = _lambda * w - res

    #learning rate
    eta = 1. / (t * _lambda)

    w -= eta * gradient_vec

    # project w back into our 1/lambda ball

    w2norm = np.linalg.norm(w, ord=2)
    w = min(1., (1. / np.sqrt(_lambda)) / w2norm) * w

    return w


# generates At+
def sortOut(A_t, w):
    x = []
    y = []
    for tuple in A_t:
        # y * <w, x> < 1
        if tuple[0] * np.dot(w, tuple[1]) < 1.:
            # only add miss classified samples
            y.append(tuple[0])
            x.append(tuple[1])
    return x, y


# generates At
def chooseRandomyfrom(S, k):
    A_t = []
    for i in range(k):
        index = int(np.random.uniform(0, len(S)))
        A_t.append(S[index])
    return A_t


#PEGASOS algorithm
# Parameter lambda - controls accuracy somehow
# Parameter k      - batch size - defines how many rows are learnt at once
#
# returns w_hat
def pegasos(_lambda, k, inpustream):
    S = []
    k = 10
    T = 100000

    # init w with zeros
    w = transform(np.random.rand(400))
    w = np.zeros(len(w))
    w[0] = 1 / np.sqrt(_lambda)

    i = 0
    for line in inpustream:
        line = line.strip()

        i += 1

        #parse a line
        y_i = 1. if line[0:1] == '+' else -1.
        x_i = np.fromstring(line[2:], sep=" ")

        # transform feature
        x_i = transform(x_i)
        S.append((y_i, x_i))

    for t in range(1, T):
        A_t = chooseRandomyfrom(S, k)
        x, y = sortOut(A_t, w)
        w = process_junk(x, y, len(x), _lambda, w, t)

    return w


if __name__ == "__main__":
    # Parameter lambda - controls accuracy somehow
    _lambda = 0.01

    # Parameter k batch size - defines how many rows are learnt at once
    k = 1000

    w_hat = pegasos(_lambda, k, sys.stdin)

    w_hat_string = " ".join([repr(s) for s in w_hat])

    # use static key 1
    print '1 \t%s' % w_hat_string
