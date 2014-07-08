#!/usr/bin/env python3

import json
import sys
import math
from utils import json_to_vectors

def cosine(bow1, bow2):
    words = set(bow1).intersection(bow2)
    dot = sum(bow1[w]*bow2[w] for w in words)
    l = math.sqrt(sum(x**2 for x in bow1.values()))*math.sqrt(sum(x**2 for x in bow2.values()))
    if l == 0:
        return 0
    else:
        return float(dot) / l

def main(filename):
    docs = []
    for id, name, bow in json.load(open('test/wiki_data.json')):
        try:
            del bow['']
        except KeyError:
            pass
        docs.append((id, name, bow))
   
    for i, (id1, name1, bow1) in enumerate(docs):
        for j, (id2, name2, bow2) in enumerate(docs[i+1:]):
            print(id1, id2, cosine(bow1, bow2))

if __name__ == '__main__':
    main(sys.argv[1])
