#!/usr/bin/python

from __future__ import division
import sys
import json
from math import *
import numpy as np

def BOPF(data):

    # Initial value
    S = data['S']
    X = data['X']
    t = data['t']
    n = data['n']
    H = data['H']
    s = data['s'] / 100  # from percentage to decimal
    r = data['r'] / 100
    k = data['k']
    u = exp(s * sqrt(t / n))
    d = 1 / u   # d = exp(-s * sqrt(t / n))
    r_ = r * t / n
    R = exp(r_)
    p = (R - d) / (u - d)  # Risk-neutral P
    MAXSUM = [[None]*(n+1)]*(n+1)
    MAXSUM = np.array(MAXSUM)
    MINSUM = [[None]*(n+1)]*(n+1)
    MINSUM = np.array(MINSUM)
    def Amax(j, i):
        if MAXSUM[j][i]!=None:
            #print(MAXSUM[j][i])
            return MAXSUM[j][i]
        #print j*100+i
        maxsum = (S * ((1 - u ** (j - i + 1)) / (1 - u) + u ** (j-i) * d * (1 - d ** i) / (1 - d) ))
        maxsum = maxsum / (j + 1)
        MAXSUM[j][i] = maxsum
        return maxsum

    def Amin(j, i):
        if MINSUM[j][i]!=None:
            #print(MINSUM[j][i])
            return MINSUM[j][i]
        minsum = (S * ((1 - d ** (i + 1)) / (1 - d) + d ** i * u * (1 - u ** (j - i)) / (1 - u) ))
        minsum = minsum / (j + 1)
        MINSUM[j][i] = minsum
        return minsum

    def Average(m, j, i):
        return (((k - m) / k) * Amin(j, i) + (m / k) * Amax(j, i))

    def findl(A, j, i):
        if A < Average(0, j, i):
            return 0
        if (A >= Average(k, j, i)):
            return k
        for l in range(k):
            if Average(l, j, i) <= A and A <= Average(l+1, j, i):
                return l
        return 0

    C = [[max(0, Average(m, n, i) - X) * (Average(m, n, i) < H) for m in xrange(k+1)] for i in xrange(n+1)]
    C = np.array(C)
    D = [None] * (k+1)
    D = np.array(D)

    # Asian barrier option
    for j in reversed(range(n)):
        print j
        for i in range(j+1):
            for m in range(k+1):
                a = Average(m, j, i)
                if a>=H:
                    D[m] = 0
                    continue
                A_u = ((j+1) * a + S * u ** (j+1-i) * d ** i) / (j+2)
                l = findl(A_u, j+1, i)
                try:
                    if l not in [0, k]:
                        x = (A_u - Average(l+1, j+1, i)) / (Average(l, j+1, i) - Average(l+1, j+1, i))
                        C_u = x * C[i][l] + (1-x) * C[i][l+1]
                    else:
                        C_u = C[i][l]
                except:
                    C_u = C[i][l]

                A_d = ((j+1) * a + S * u ** (j-i) * d ** (i+1)) / (j+2)
                l = findl(A_d, j+1, i+1)
                try:
                    if l not in [0, k]:
                        x = (A_d - Average(l+1, j+1, i+1)) / (Average(l, j+1, i+1) - Average(l+1, j+1, i+1))
                        C_d = x * C[i+1][l] + (1-x) * C[i+1][l+1]
                    else:
                        C_d = C[i+1][l]
                except:
                    C_d = C[i+1][l]

                D[m] = max(((p * C_u + (1-p) * C_d) / R), a-X, 0)

            C[i][:] = D[:]

    print C[0][0]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location) as data_file:
            data = json.load(data_file)
        for test in data:
            BOPF(test)
        print "finished!"
    else:
        print 'Requires an input file. (e.g. python hw2.py data)'