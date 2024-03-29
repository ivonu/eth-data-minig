#!/usr/bin/env python2.7
import sys

import numpy as np
import sklearn.cluster as sklearn

if len(sys.argv) > 1:
    sys.stdin = open(sys.argv[1], 'r')


if __name__ == "__main__":

    S = []
    for line in sys.stdin:
        line = line[2:]
        split = line.split('\t', 1)
        weight = int(split[0])
        line = split[1]
        line = line.strip()
        #parse a line
        x_t = np.fromstring(line, sep=" ")
        S.append(x_t)

    data = np.array(S)
    S = []
    mu = sklearn.k_means(data, n_clusters=200, n_jobs=1)
    for mu_i in mu[0]:
        print_string = " ".join([repr(s) for s in mu_i])
        print '%s' % print_string
