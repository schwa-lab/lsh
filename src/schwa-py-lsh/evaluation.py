#!/usr/bin/env python3

"""
Evaluation for LSH v. cosine.
"""

import argparse
from datetime import datetime
from utils import json_to_vectors
from hashes import Projection

def main(args):
    vecs = json_to_vectors(open(args.json))
    proj = Projection(args.bits, len(vecs[0]))
    sigs = []
    for vec in vecs:
        sigs.append(proj.hash(vec))
        

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('json', help='File containing (id1, name, bow) for documents.')
    p.add_argument('cosine', help='File containing (id1, id2, cosine) for documents.')
    p.add_argument('-b', '--bits', default=128, type=int, help='Number of permutations.')
    p.add_argument('-p', '--permutations', default=10, type=int, help='Number of permutations for kNN.')
    p.add_argument('-l', '--permutation-length', default=5, type=int, help='Number of bits for permutations for kNN.')
    p.add_argument('-w', '--window-size', default=10, type=int, help='Window size for each permutation for kNN.')
    p.add_argument('-k', '--k-nearest-neighbours', default=1, type=int, help='Number of k nearest neighbours to evaluate over.')
    args = p.parse_args()
    
    main(args)
