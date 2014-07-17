#!/usr/bin/env python3

"""
Evaluation for LSH v. cosine.
"""

import math
import argparse
from datetime import datetime
from lsh.query import KNNQuery
import cProfile, pstats, io

NBITS_HEADER = "consts.pxi"
BASE_SIZE = 64 # size of unsigned long long

def cosine(bow1, bow2):
    words = set(bow1).intersection(bow2)
    dot = sum(bow1[w]*bow2[w] for w in words)
    l = math.sqrt(sum(x**2 for x in bow1.values()))*math.sqrt(sum(x**2 for x in bow2.values()))
    if l == 0:
        return 0
    else:
        return float(dot) / l

def run_cosine(queries, items, query_item):
    s = []
    for id in queries:
        sim = cosine(items[id].bow, query_item.bow)
        s.append((sim, id))
    s.sort(reverse=True)
    return s

def proportion_correct(neighbours, candidates, neighbours_k, knn_k):
    # print('neighbours:{}\tcandidates:{}\n'.format(neighbours, [(x.data, x.working) for x in candidates[0][0].signature.hashes] if candidates else []))
    intersection = set(n[0] for n in neighbours[:neighbours_k]).intersection(set(c for c in candidates[:knn_k]))
    return intersection

def run_queries(args, items, correct=None):
    queries = {}
    k = KNNQuery(args.permutations, args.bits, args.window_size, int(args.bits/64), args.prefix_length, args.shuffle_perms, args.reset_before_shuffle)
    for item in items.values():
        k.add_item_to_index(item)
    count = 0
    print("Starting queries")
    queries = k.find_all_neighbours(item, args.knn_k, correct)
    return queries

def sort_queries(queries, items, query_signature):
    return sorted(queries, key=lambda x: items[x].signature.bits_in_common(query_signature), reverse=True)

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
    print('Generating hashes took: {}'.format(datetime.now() - start))
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

    start = datetime.now()
    queries = run_queries(args, items, correct_candidates if args.debug else None)
    print('Running queries took {}'.format(datetime.now() - start))

    if args.profile:
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

    total_candidates = 0
    print ("Processing candidates")
    start = datetime.now()
    for id in correct_candidates:
        queries[id] = sort_queries(queries[id], items, items[id].signature)
        intersection = proportion_correct(correct_candidates[id], queries[id], args.neighbours_k, args.knn_k)
        correct += len(intersection)
        total_candidates += min(len(queries[id]), args.knn_k)
        total += len(neighbours[:args.neighbours_k])
    print('Processing candidates took {}'.format(datetime.now() - start))
    print ("Running cosine")
    start = datetime.now()
    correct_cosine = 0
    total_cosine = 0
    for id in correct_candidates:
        s = run_cosine(queries[id][:args.knn_k], items, items[id])
        total_cosine += min(args.neighbours_k, len(correct_candidates[id]))
        correct_cosine += len(set(n[0] for n in correct_candidates[id][:args.neighbours_k]).intersection(set(c[1] for c in s)))
    print('Running cosine took {}'.format(datetime.now() - start))
    cosine_metric = correct_cosine / total_cosine * 100
    metric =  correct / total * 100
    max_candidates = len(queries)
    avg_candidates = total_candidates / max_candidates
    print('bits:{}-perms:{}-prefix:{}-window:{}-knn-k:{}-neighbours-k:{} gave recall metric of {} with an average of {} candidates ({} total queries): {} total cosine coverage'.format(args.bits, args.permutations, args.prefix_length, args.window_size, args.knn_k, args.neighbours_k, metric, avg_candidates, max_candidates, cosine_metric))

def write_nbits(nbits):
    """We have to write out the size N to a pxi file for cython to import"""
    if nbits % BASE_SIZE != 0:
        raise RuntimeError("bits must be a multiple of {}".format(BASE_SIZE))
    with open(NBITS_HEADER, 'w') as f:
        f.write("DEF N = {}\n".format(int(nbits / BASE_SIZE)))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('json', help='File containing (id1, name, bow) for documents.')
    p.add_argument('cosine', help='File containing (id1, id2, cosine) for documents.')
    p.add_argument('-b', '--bits', default=64, type=int, help='Number of permutations.')
    p.add_argument('-p', '--permutations', default=10, type=int, help='Number of permutations for kNN.')
    p.add_argument('-w', '--window-size', default=10, type=int, help='Window size for each permutation for kNN.')
    p.add_argument('-k', '--knn-k', default=1, type=int, help='Number of query k nearest neighbours to evaluate over.')
    p.add_argument('-n', '--neighbours-k', default=10, type=int, help='Number of cosine nearest neighbours to evaluate over.')
    p.add_argument('-l', '--prefix-length', default=5, type=int, help='Default length of prefix of hash to use')
    p.add_argument('-s', '--shuffle-perms', default=100, type=int, help='Shuffle hashes randomly after this number of permutations')
    p.add_argument('-r', '--reset-before-shuffle', default=False, action='store_true', help='Reset hashes to their original value before shuffling')
    p.add_argument('--no-json', action='store_true', help='Use precomputed hash file')
    p.add_argument('--profile', action='store_true', default=False, help='Profile the performance')
    p.add_argument('--debug', action='store_true', default=False, help='Print debugging information')
    args = p.parse_args()

    write_nbits(args.bits)

    main(args)
