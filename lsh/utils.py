#!/usr/bin/env python3

import json
from lsh.model import LSHItem
from lsh.hashes import Projection, Hashes

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
    n_proj = bits//64
    proj = []
    for i in range(n_proj):
        proj.append(Projection(bits, len(vectors[0][1])))
    for id, v in vectors:
        h = Hashes()
        for p in proj:
            h.append(p.hash(v))
        print(v, [x.get_data() for x in h.hashes])
        yield LSHItem(id, h, vector = v)


def json_to_items(filelike, bits):
    return vectors_to_items(json_to_vectors(filelike), bits)


