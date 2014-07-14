#!/usr/bin/env python3

"""
Evaluation for LSH v. cosine.
"""

import argparse
from datetime import datetime
from lsh.query import KNNQuery
import cProfile, pstats, io

NBITS_HEADER = "consts.pxi"
BASE_SIZE = 64 # size of unsigned long long

def proportion_correct(neighbours, candidates, k):
    # print('neighbours:{}\tcandidates:{}\n'.format(neighbours, [(x.data, x.working) for x in candidates[0][0].signature.hashes] if candidates else []))
    intersection = set(n[0] for n in neighbours[:k]).intersection(set(c[0].id for c in candidates[:k]))
    return len(intersection)/k

def run_queries(args, items, correct=None):
    queries = {}
    start = datetime.now()
    print ("Loading NN query")
    k = KNNQuery(args.permutations, args.bits, args.window_size, int(args.bits/64), args.prefix_length)
    print("Done",datetime.now()-start)
    for item in items.values():
        k.add_item_to_index(item)
    count = 0
    print("Starting queries")
    queries = k.find_all_neighbours(item, args.k_nearest_neighbours, correct)
    stop = datetime.now()
    print('Running queries took {}'.format(stop - start))
    return queries

from lsh.readers import LSHReader
def main(args):
    from lsh.hashes import Projection
    from lsh.utils import json_to_items
    print('json:{}'.format(args.json))
    start = datetime.now()
    # read in a list of LSHItems
    if args.no_json:
        r = LSHReader()
        items = list(r.process_file(open(args.json)))
    else:
        items = list(json_to_items(open(args.json)))
    stop = datetime.now()
    print('Generating hashes took: {}'.format(stop - start))
    # map id to item
    items = dict((item.id, item) for item in items)
    correct = 0
    total = 0
    if args.profile:
        pr = cProfile.Profile()
        pr.enable()

    correct_candidates = {}

    for line in open(args.cosine):
        line = line.strip().split('\t')
        id = int(line[0])
        # neighbours: [ [id1, cosine1], [id2, cosine2] ... ]
        neighbours = [i.split(' ') for i in line[1:]]
        neighbours = [(int(id), float(cosine)) for id, cosine in neighbours]
        correct_candidates[id] = neighbours

    queries = run_queries(args, items, correct_candidates if args.debug else None)

    if args.profile:
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

    total_candidates = 0
    for id in correct_candidates:
        correct += proportion_correct(correct_candidates[id], queries[id], args.k_nearest_neighbours)
        total_candidates += len(queries[id])
        total += 1
    metric =  correct / total
    max_candidates = len(queries)
    avg_candidates = total_candidates / max_candidates
    print('bits:{}-perms:{}-prefix:{}-window:{}-k:{} gave recall metric of {} with an average of {} candidates ({} total queries)'.format(args.bits, args.permutations, args.prefix_length, args.window_size, args.k_nearest_neighbours, metric, avg_candidates, max_candidates))

def write_nbits(nbits):
    """We have to write out the size N to a pxi file for cython to import"""
    with open(NBITS_HEADER, 'w') as f:
        f.write("DEF N = {}\n".format(int(nbits / BASE_SIZE)))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('json', help='File containing (id1, name, bow) for documents.')
    p.add_argument('cosine', help='File containing (id1, id2, cosine) for documents.')
    p.add_argument('-b', '--bits', default=64, type=int, help='Number of permutations.')
    p.add_argument('-p', '--permutations', default=10, type=int, help='Number of permutations for kNN.')
    p.add_argument('-w', '--window-size', default=10, type=int, help='Window size for each permutation for kNN.')
    p.add_argument('-k', '--k-nearest-neighbours', default=1, type=int, help='Number of k nearest neighbours to evaluate over.')
    p.add_argument('-r', '--prefix-length', default=5, type=int, help='Default length of prefix of hash to use')
    p.add_argument('--no-json', action='store_true', help='Use precomputed hash file')
    p.add_argument('--profile', action='store_true', default=False, help='Profile the performance')
    p.add_argument('--debug', action='store_true', default=False, help='Print debugging information')
    args = p.parse_args()

    write_nbits(args.bits)

    main(args)
