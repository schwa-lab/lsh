#!/usr/bin/env python3

import json

BITS = 128

def json_to_vectors(filelike):
    """
    Load json file, calculate feature space, convert to vectors.
    """

    f_space = set()
    docs = []
    for id, name, bow in json.load(open('test/wiki_data.json')):
        try:
            del bow['']
        except KeyError:
            pass
        docs.append((id, name, bow))
        f_space |= set(bow.keys())

    f_space = filter(lambda x: x, f_space) # remove empty strings
    # vectors are sparse so we want to lookup into them directly
    f_space = dict(((v, k) for k, v in enumerate(f_space)))

    length = len(f_space.keys())

    vectors = []
    for id, name, bow in docs:
        vec = [0 for x in range(length)]
        for word, count in bow.items():
            if not word: # remove empty strings, again
                continue
        vectors.append((id, vec))

    return vectors


#def vectors_to_items(vectors):
