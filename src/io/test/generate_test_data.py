#!/usr/bin/env python3

"""
Generate test pairs.

Usage: ./generate_test_data.py n
    n: number of lines to generate
"""

import sys
import random

def main(n):
    for i in range(n):
        print(i * 100, "{0:b}".format(random.getrandbits(128)))

if __name__ == '__main__':
    main(int(sys.argv[1]))
