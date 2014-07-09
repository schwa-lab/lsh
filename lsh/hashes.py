#!/usr/bin/python3
import numpy, sys
from bitstring import BitArray
#from test.generate_test_vectors import TestVectorGenerator
import pyximport; pyximport.install()
from lsh import bits

class Projection:
    def __init__(self, n_bits, n_feats):
        self.n_bits = n_bits
        self.n_feats = n_feats
        self.vectors = numpy.random.randn(self.n_bits, self.n_feats)

    def hash(self, v):
        h = numpy.dot(self.vectors, v)
        h = ''.join('1' if x > 0 else '0' for x in h)
        return int(h[:64],2)

class Hashes:
    def __init__(self,sig=False):
        self.hashes = []
        if sig:
            for x in [sig[i:i+64] for i in range(0, len(sig), 64)]:
                self.append(int(x,2))
           
    def append(self, x):
         self.hashes.append(bits.Hash(x))

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


import json
def test_json():
    BITS = 128

    f_space = set()
    docs = []
    for id, name, bow in json.load(open('test/wiki_data.json')):
        docs.append((id, name, bow))
        f_space |= set(bow.keys())

    f_space = filter(lambda x: x, f_space) # remove empty strings
    # vectors are sparse so we want to lookup into them directly
    f_space = dict(((v, k) for k, v in enumerate(f_space)))

    length = len(f_space.keys())

    proj = Projection(BITS, length)
    for id, name, bow in docs:
        vec = [0 for x in range(length)]
        for word, count in bow.items():
            if not word: # remove empty strings, again
                continue
            vec[f_space[word]] = count
        print(id, proj.hash(vec).bin)

if __name__ == '__main__':
    #main(int(sys.argv[1]))
    test_json()
