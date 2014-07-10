"""
Simple hash container with a basic bitwise left rotate operation
"""


DEF BITS_IN_CHAR = 8

cdef class Hash:
    cdef public unsigned long data
    cdef public unsigned long working

    def __cinit__(self, data):
        self.data = data
        self.working = data

    cpdef lrotate(self, unsigned int shift):
        self.working = (self.working << shift) | (self.working >> (sizeof(self.working) * BITS_IN_CHAR - shift))

    cpdef rrotate(self, unsigned int shift):
        """Doesn't seem to work :("""
        self.working = (self.working >> shift) | (self.working << (sizeof(self.working) * BITS_IN_CHAR - shift))

    cpdef long get_prefix(self, unsigned int length) except *:
        # for i in range((sizeof(x) * BITS_IN_CHAR) - length):
            # print(i, length, x, self.get_bitstring(x), x >> 1, self.get_bitstring(x >> 1))
        return self.working >> ((sizeof(self.working) * BITS_IN_CHAR) - length)

    def get_bitstring(self, unsigned long bits):
        cdef int i
        cdef unsigned long o
        x = ""
        o = 1
        for i in range(sizeof(bits) * BITS_IN_CHAR):
            if o & bits:
                x = "1" + x
            else:
                x = "0" + x
            o <<= 1
        return x

    def print_bitstring(self, unsigned long bits):
        print(self.get_bitstring(bits))

    def __richcmp__(Hash self, Hash other, int op):
        if op == 0:
            return self.working < other.working
        return 0

