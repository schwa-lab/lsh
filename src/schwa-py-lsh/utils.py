#!/usr/bin/env python3

import json
from .model import LSHItem
from .hashes import Projection

BITS = 128

def json_to_vectors(filelike):
    """
    Load json file, calculate feature space, convert to vectors.
    """

    f_space = set()
    docs = []
    for id, name, bow in json.load(filelike):
        try:
            del bow['']
        except KeyError:
            pass
        docs.append((int(id), name, bow))
        f_space |= set(bow.keys())

    # vectors are sparse so we want to lookup into them directly
    f_space = dict(((v, k) for k, v in enumerate(f_space)))

    length = len(f_space.keys())

    for id, name, bow in docs:
        vec = [0 for x in range(length)]
        for word, count in bow.items():
            if not word: # remove empty strings, again
                continue
            vec[f_space[word]] = count 
        yield (id, vec)


def vectors_to_items(vectors, bits):
    vectors = list(vectors)
    proj = Projection(bits, len(vectors[0][1]))
    for id, v in vectors:
        yield LSHItem(id, proj.hash(v), vector = v)


def json_to_items(filelike, bits):
    return vectors_to_items(json_to_vectors(filelike), bits)


