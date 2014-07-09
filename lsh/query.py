#!/usr/bin/env python3

import random

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

class KNNQuery(object):
    def __init__(self, perm_num, perm_length, sig_length, window_size, n_hashes, prefix_length):
        self.generate_perms(perm_num, perm_length, sig_length)
        self.window_size = window_size
        self.items = []
        self.n_hashes = n_hashes
        self.prefix_length = prefix_length

    def find_neighbours(self, query_item, k):
        candidates = defaultdict(int)
        for perm in self.perms:
            for i in range(self.n_hashes): # TODO: make this global, or parsed into query object etc
                buckets = defaultdict(list)
                query_prefix = ""
                for item in self.items:
                    #rep = ''
                    #for bit_index in perm:
                    #    rep += str(int(item.signature[bit_index]))
                    h = item.signature.hashes[i]
                    h.lrotate(perm)
                    prefix = h.get_prefix(self.prefix_length)
                    buckets[prefix].append(item)
                    if item.id == query_item.id:
                        query_prefix = prefix
                self.add_candidates(buckets, candidates, query_item, query_prefix)
        sorted_candidates = sorted(candidates.items(), key=itemgetter(1), reverse=True)
        return sorted_candidates[:k]

    def add_candidates(self, buckets, candidates, query_item, query_prefix):
        ncandidates = self.window_size * 2
        nadded = 0
        for item in buckets[query_prefix]:
            candidates[item] += 1
            nadded += 1
        prefix_index = 0
        while nadded <= ncandidates and prefix_index < self.prefix_length:
            prefix = query_prefix ^ (1 << prefix_index)
            for item in buckets[prefix]:
                candidates[item] += 1
                nadded += 1
            prefix_index += 1

    def add_items_to_index(self, filelike):
        r = LSHReader()
        for item in r.process_file(filelike):
            self.add_item_to_index(item)

    def add_item_to_index(self, item):
        self.items.append(item)

    def generate_perms(self, perm_num, perm_length, sig_length):
        self.perm_length = perm_length
        self.perms = []
        ints = list(range(sig_length))
        random.shuffle(ints)
        total_rot = 0
        for r in ints:
            if not total_rot + r % sig_length:
                continue
            total_rot += r
            self.perms.append(r)
            if len(self.perms) == perm_length:
                break

        

if __name__ == '__main__':
    TESTFILE = './schwa-py-lsh/test/test_data_1000.txt'
    q = KNNQuery(perm_num=10, perm_length=5, sig_length=100, window_size=10)
    q.add_items_to_index(open(TESTFILE, 'r'))
    for item in q.items:
        print(str(item))
        print('\n'.join(str(n) for n in q.find_neighbours(item, 10)))
        print()
