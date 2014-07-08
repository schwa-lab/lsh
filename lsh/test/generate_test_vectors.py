#!/usr/bin/env python3

"""
Generate test vectors.

Usage: ./generate_test_data.py n
    n: number of lines to generate
"""

import sys
import random

class TestVectorGenerator:
    def __init__(self):
        self.id = 0
    
    def get(self):
        self.id += 1
        return self.id, [random.randint(0, 100) for x in range(1000)]

def main(n):
    t = TestVectorGenerator()
    for i in range(n):
        print(t.get())

if __name__ == '__main__':
    main(int(sys.argv[1]))
