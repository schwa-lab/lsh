#!/usr/bin/env python3

import sys
import math
from collections import defaultdict

def main(filename):
    pairs = defaultdict(list)
    for line in open('cosine.txt'):
        id1, id2, cosine = line.strip().split(' ')
        cosine = float(cosine)
        pairs[id1].append((id2, cosine))
        pairs[id2].append((id1, cosine))
 
    for id, neighbours in pairs.items():
        # get 10 nearest neighbours and print
        print('{}\t{}'.format(id, '\t'.join(('{} {}'.format(x[0], x[1]) for x in sorted(neighbours, key=lambda x: x[1], reverse=True)[:10]))))

if __name__ == '__main__':
    main(sys.argv[1])
