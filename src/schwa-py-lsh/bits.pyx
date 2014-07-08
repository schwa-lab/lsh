"""

usage example

import pyximport; pyximport.install()

import this_module
l = range(this_module.ARRAY_SIZE)
import random
random.shuffle(l)
index = this_module.Index(l)
index.permute(555)
"""


DEF N = 4
ARRAY_SIZE = N

cdef class Hash:
    cdef unsigned int[N] permutation # 32 x N bit array

    def __cinit__(self, permutation):
        assert len(permutation) == N
        for i in range(N):
            self.permutation[i] = permutation[i]
            #self.permutation[i] = 2 ** permutation[i]

    def permute(self, unsigned int x):
        cdef unsigned int out = 0
        cdef unsigned int offset = 1
        for i in range(N):
            if x & self.permutation[i]:
                out |= offset
            offset = offset << 1
        return out
