#!/usr/bin/env python3

import math
import random
from datetime import datetime

from operator import itemgetter
from collections import defaultdict

from lsh.model import LSHItem
from lsh.readers import LSHReader
from lsh.writers import LSHWriter


"""

KNNQuery needs to run in two modes:
    INDEX   items are given to the object for storage 
    QUERY   given a LSHItem id, return the k-nearest neighbours in the index, with counts populated

"""

def compute_sim(lshash1, lshash2, hash_length):
    diff_bits = lshash1 ^ lshash2
    while diff_bits:
        diff_bits &= diff_bits - 1 # Clear the least significant bit set
        hash_length -= 1
    return hash_length

def cosine_sim(bow1, bow2):
    dot = sum(x * y for x, y in zip(bow1, bow2))
    l = math.sqrt(sum(x**2 for x in bow1)) * math.sqrt(sum(x**2 for x in bow2))
    if l==0:
        return 0
    else:
        return float(dot) / l

class KNNQuery(object):
    def __init__(self, perm_num, sig_length, window_size, n_hashes, prefix_length, shuffle_perms, reset_before_shuffle):
        self.generate_perms(perm_num, sig_length)
        self.window_size = window_size
        self.items = []
        self.sig_length = sig_length
        self.n_hashes = n_hashes
        self.prefix_length = prefix_length
        self.shuffle_perms = shuffle_perms
        self.reset_before_shuffle = reset_before_shuffle

    def find_all_neighbours(self, query_item, k, correct=None):
        if correct is None:
            correct = {}
        neighbours = {}
        candidates = defaultdict(lambda: defaultdict(int))
        start = datetime.now()
        shuffle = False
        for i, perm in enumerate(self.perms):
            buckets = defaultdict(list)
            prefixes = {}
            if i:
                if i % 100 == 0:
                    print("Processed {} permutations, Total time: {}".format(i, datetime.now() - start))
                if i % self.shuffle_perms == 0:
                    shuffle = True
                    randoms = [random.randint(i, self.sig_length-1) for i in range(self.sig_length)]
                else:
                    shuffle = False

            # do the hashing
            for item in self.items:
                h = item.signature
                h.lrotate(perm)
                if shuffle:
                    h.shuffle(randoms)
                prefix = h.get_prefix(self.prefix_length)
                prefixes[item.id] = prefix
                buckets[prefix].append(item)

            # do the lookup-ing
            for item in self.items:
                query_prefix = prefixes[item.id]
                self.add_candidates(buckets, candidates[item.id], item, query_prefix, correct)

        # for id in candidates:
        #     candidates[id] = sorted(candidates[id].items(), key=itemgetter(1), reverse=True)

        if correct:
            self.print_debug(query_item, candidates, correct)
        return candidates

    def print_debug(self, query_item, sorted_candidates, correct=None):
        for candidate in sorted_candidates:
            cosine = cosine_sim(query_item.vector, candidate[0].vector)
            if cosine > 0.1:
                print("XOR similarity:", compute_sim(query_item.signature.get_first_working(), candidate[0].signature.get_first_working(), self.sig_length), "Cosine similarity:", cosine)

    def add_candidates(self, buckets, candidates, query_item, query_prefix, correct=None):
        if correct is None:
            correct = []
        ncandidates = self.window_size * 2
        nadded = 0
        for item in buckets[query_prefix]:
            if item.id != query_item.id:
                candidates[item.id] += 1
                nadded += 1
        prefix_index = 0
        while nadded <= ncandidates and prefix_index < self.prefix_length:
            prefix = query_prefix ^ (1 << prefix_index)
            for item in buckets[prefix]:
                candidates[item.id] += 1
                nadded += 1
            prefix_index += 1

    def add_items_to_index(self, filelike):
        r = LSHReader()
        for item in r.process_file(filelike):
            self.add_item_to_index(item)

    def add_item_to_index(self, item):
        self.items.append(item)

    def generate_perms(self, perm_num, sig_length):
        self.perms = list(random.randint(1, sig_length - 1) for i in range(perm_num))
        random.shuffle(self.perms)


if __name__ == '__main__':
    TESTFILE = './schwa-py-lsh/test/test_data_1000.txt'
    q = KNNQuery(perm_num=10, sig_length=100, window_size=10)
    q.add_items_to_index(open(TESTFILE, 'r'))
    for item in q.items:
        print(str(item))
        print('\n'.join(str(n) for n in q.find_neighbours(item, 10)))
        print()
