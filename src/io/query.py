#!/usr/bin/env python3

import random

from operator import itemgetter
from collections import defaultdict

from .model import LSHItem
from .readers import LSHReader
from .writers import LSHWriter


"""

KNNQuery needs to run in two modes:
    INDEX   items are given to the object for storage 
    QUERY   given a LSHItem id, return the k-nearest neighbours in the index, with counts populated

"""

def binary_search(seq, target):
    lower = 0
    upper = len(seq) - 1
    while True:
        if upper < lower: return -1
        m = (lower + upper) // 2
        if seq[m][1] < target:
            lower = m + 1
        elif seq[m][1] > target:
            upper = m - 1
        else:
            return m



class KNNQuery(object):
    def __init__(self, perm_num, perm_length, sig_length, window_size):
        self.generate_perms(perm_num, perm_length, sig_length)
        self.window_size = window_size
        self.items = []


    def find_neighbours(self, query_item, k):
        candidates = defaultdict(int)
        for perm in xrange(self.perms):
            reps = []
            for item in self.items:
                rep = ''
                for bit_index in perm:
                    rep += str(item.signature[bit_index])
                reps.append((rep, item))
            reps.sort()
            idx = self.find_query_item(reps, query_item)
            lower = idx - self.window
            if lower < 0:
                lower = 0
            upper = idx + self.window + 1
            self.add_candidates(reps[lower:upper], candidates)
        sorted_candidates = sorted(candidates.items(), key=itemgetter(1), reverse=True)
        return sorted_candidates[:k]


    def add_candidates(self, reps, candidates):
        for rep in reps:
            candidates[rep[1]] += 1
        

    def find_query_item(self, reps, query_item):
        idx = binary_search(reps, query_item)
        assert idx != -1, "Could not find index of {} in permutation".format(query_item)
        return idx


    def add_items_to_index(self, filelike):
        r = LSHReader()
        for item in r.process_document(filelike):
            self.add_item_to_index(item)


    def add_item_to_index(self, item):
        self.items.append(item)


    def generate_perms(self, perm_num, perm_length, sig_length):
        self.perms = []
        ints = list(range(sig_length))
        for perm in range(perm_num):
            self.perms.append(random.shuffle(ints)[:perm_length])


if __name__ == '__main__':
    TESTFILE = './io/test/test_data_1000.txt'
    q = KNNQuery(perm_num=2, perm_length=10, sig_length=100, window_size=5)
    q.add_items_to_index(open(TESTFILE, 'r'))
    for item in q.items:
        print(str(item))
        print('\n'.join(str(n) for n in q.find_neighbours(item, 2)))
        print()
