#!/usr/bin/env python3

"""
Evaluation for LSH v. cosine.
"""

import argparse
from datetime import datetime
from utils import json_to_items
from hashes import Projection
from query import KNNQuery


def proportion_correct(neighbours,candidates):
    intersection = set(n[0] for n in neighbours).intersection(set(c[0].id for c in candidates))
    return float(len(intersection))/(len(neighbours))
        

def run_queries(args):
    queries = {}
    start = datetime()
    k = KNNQuery(args.permutations, args.permutation-length, args.bits, args.window-size)
    for line in open(args.cosine):
        line = line.strip().split('\t')
        id = line[0]
        queries[id] = k.find_neigbours(items[id], args.k-nearest-neighbours)
    stop = datetime()
    print('Running queries took {}'.format(stop - start))
    return queries


def main(args):
    print('json:{}'.format(args.json))
    start = datetime()
    items = json_to_items(open(args.json))
    stop = datetime()
    print('Generating hashes took: {}'.format(stop- start))
    items = dict(item.id, item for item in items)
    correct = 0
    total = 0
    queries = run_queries(args)
    for id, candidates in queries.items():
        # neighbours: [ [id1, cosine1], [id2, cosine2] ... ]
        neighbours = [item.split(' ') for item in line[1:]]
        correct += proportion_correct(neighbours, candidates)
        total += 1
    metric =  correct / total
    print('bits:{}-perms:{}-length:{}-window:{}-k:{} gave precision metric of {}'.format(args.bits, args.permutations, args.permutation-length, args.window-size, args.k-nearest-neighbours, metric))


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
