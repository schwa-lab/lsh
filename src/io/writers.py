#!/usr/bin/env python3

"""
Write a human-readable format for a bit representation
"""

import sys
from human_reader import LSHReader

class LSHWriter(object):
    def __init__(self):
        pass

    def process_item(self, item):
        return item.id,item.signature.bin

    def process_items(self, items):
        for item in items:
            yield self.process_item(item)

def main(filename):
    r = LSHReader()
    items = r.process_document(open(filename))
    w = LSHWriter()
    for id, sig in w.process_items(items):
        print(id,sig)

if __name__ == '__main__':
    main(sys.argv[1]) # filename
