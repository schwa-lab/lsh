#!/usr/bin/env python3

"""
Read human-readable representation of lsh_items to bits.
"""

import sys

def main(filename):
    for line in open(filename):
        id, hash = line.strip().split(' ')
        id = int(id)

if __name__ == '__main__':
    main(sys.argv[1]) # filename
