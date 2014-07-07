#!/usr/bin/python3
import numpy
from bitstring import BitArray

class Projection:
    def __init__(self, n_bits, n_feats):
        self.n_bits = n_bits
        self.n_feats = n_feats
        self.vectors = numpy.random.randn(self.n_bits, self.n_feats)

    def hash(self, v):
        h = numpy.dot(self.vectors, v)
        h = [1 if x > 0 else 0 for x in h]
        return BitArray(h)


