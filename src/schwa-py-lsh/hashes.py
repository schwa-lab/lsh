#!/usr/bin/python3
import numpy, sys
from bitstring import BitArray
from test.generate_test_vectors import TestVectorGenerator

class Projection:
    def __init__(self, n_bits, n_feats):
        self.n_bits = n_bits
        self.n_feats = n_feats
        self.vectors = numpy.random.randn(self.n_bits, self.n_feats)

    def hash(self, v):
        h = numpy.dot(self.vectors, v)
        h = [x > 0 for x in h]
        return BitArray(h)



def main(n_vecs):
   generator = TestVectorGenerator()
   proj = Projection(100, 1000)
   for n in range(n_vecs):
       id, vec = generator.get()
       signature = proj.hash(vec)
       print(id, vec)
       print(signature.bin)

def test_random_vecs(n_vecs):
   generator = TestVectorGenerator()
   for n in range(n_vecs):
       id, vec = generator.get()
       proj = Projection(100, 1000)
       signature = proj.hash(vec)
       print(id, vec)
       print(signature.bin)
       # Change half the bits
       for i in range(500):
           vec[i] = 1
       signature2 = proj.hash(vec)
       print(signature2.bin)
       print(signature == signature2)
       print(len((signature ^ signature2).bin.replace('0', '')))


if __name__ == '__main__':
    main(int(sys.argv[1]))
