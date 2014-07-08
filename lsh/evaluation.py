#!/usr/bin/env python3

"""
Evaluation for LSH v. cosine.
"""

import argparse
from datetime import datetime
from .utils import json_to_items
from .hashes import Projection
from .query import KNNQuery


def proportion_correct(neighbours, candidates):
    #print('neighbours:{}\tcandidates:{}'.format(neighbours, candidates))
    intersection = set(n[0] for n in neighbours).intersection(set(c[0].id for c in candidates))
    return float(len(intersection))/(len(neighbours))
        

def run_queries(args, items):
    queries = {}
    start = datetime.now()
    k = KNNQuery(args.permutations, args.permutation_length, args.bits, args.window_size)
    for item in items.values(): 
        k.add_item_to_index(item)
    for item in items.values(): 
        if item.id > 10: continue
        queries[item.id] = k.find_neighbours(item, args.k_nearest_neighbours)
    stop = datetime.now()
    print('Running queries took {}'.format(stop - start))
    return queries

from .readers import LSHReader
def main(args):
    print('json:{}'.format(args.json))
    start = datetime.now()
    #items = list(json_to_items(open(args.json),args.bits))
    r = LSHReader()
    items = list(r.process_file(open(args.json)))
    stop = datetime.now()
    print('Generating hashes took: {}'.format(stop - start))
    items = dict((item.id, item) for item in items)
    correct = 0
    total = 0
    import cProfile, pstats, io
    pr = cProfile.Profile()
    pr.enable()
    queries = run_queries(args, items)
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    for line in open(args.cosine):
        line = line.strip().split('\t')
        id = int(line[0])
        # neighbours: [ [id1, cosine1], [id2, cosine2] ... ]
        neighbours = [i.split(' ') for i in line[1:]]
        neighbours = [(int(id), float(cosine)) for id, cosine in neighbours]
        correct += proportion_correct(neighbours, queries[id])
        total += 1
    metric =  correct / total
    print('bits:{}-perms:{}-length:{}-window:{}-k:{} gave precision metric of {}'.format(args.bits, args.permutations, args.permutation_length, args.window_size, args.k_nearest_neighbours, metric))


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
