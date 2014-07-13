"""
Simple hash container with a basic bitwise left rotate operation
"""

include "consts.pxi"

DEF BITS_IN_CHAR = 8

cpdef NBITS():
    #Stupid function to return the number of bits in the hash
    return BITS_IN_CHAR * N * sizeof(unsigned long long)

cdef class Hash:
    cdef unsigned long long data[N]
    cdef unsigned long long working[N]
    cdef public unsigned long long size
    cdef public unsigned long long nbits

    def __cinit__(self, bits):
        self.size = sizeof(unsigned long long) * BITS_IN_CHAR
        self.nbits = N * self.size
        cdef unsigned long long i
        cdef unsigned long long index = 0
        cdef unsigned long long slot
        cdef unsigned long long shifter = 1
        self.data[0] = 0
        self.working[0] = 0

        # assume bits is of correct length
        for i, bit in enumerate(bits):
            slot = i % self.size
            if i > 0 and slot == 0:
                index += 1
                self.data[index] = 0
                self.working[index] = 0
            slot = self.size - slot - 1
            if bit:
                self.data[index] |= (shifter << slot)
                self.working[index] |= (shifter << slot)
            else:
                self.data[index] &= ~(shifter << slot)
                self.working[index] &= ~(shifter << slot)

    cpdef reverse(self, int low, int high):
        cdef unsigned long long left = self.working[low]
        cdef unsigned long long right = self.working[high]
        cdef unsigned long long temp
        while low < high:
            temp = self.working[low]
            self.working[low] = self.working[high]
            self.working[high] = temp
            low += 1
            high -= 1

    cpdef lassign(self, int assign):
        self.reverse(0, N)
        self.reverse(0, N - assign)
        self.reverse(N - assign, N)

    cpdef lrotate(self, unsigned long long shift):
        cdef int i = N - 1
        cdef int assign = 0

        if shift == self.size * N or shift == 0:
            return
        elif shift >= self.size:
            assign = shift // self.size
            shift %= self.size
            assign %= N
            if assign != 0:
                self.lassign(assign)
            if shift == 0:
                return

        cdef unsigned long long reverse_shift = (self.size - shift) % self.size
        cdef unsigned long long carry = self.working[0] >> (reverse_shift)

        while i >= 0:
            new_carry = self.working[i] >> (reverse_shift)
            self.working[i] = (self.working[i] << shift) | carry
            carry = new_carry
            i -= 1

    cpdef unsigned long long get_prefix(self, unsigned long long length) except *:
        return self.working[0] >> (self.size - length)

    cpdef unsigned long long get_first_data(self):
        return self.data[0]

    cpdef unsigned long long get_first_working(self):
        return self.working[0]

    def get_original_hash(self):
        cdef int i = N - 1
        x = ""
        while i >= 0:
            o = 1
            for j in range(self.size):
                if o & self.data[i]:
                    x = "1" + x
                else:
                    x = "0" + x
                o <<= 1
            i -= 1
        return x

    def get_working_hash(self):
        cdef int i = N - 1
        x = ""
        while i >= 0:
            o = 1
            for j in range(self.size):
                if o & self.working[i]:
                    x = "1" + x
                else:
                    x = "0" + x
                o <<= 1
            i -= 1
        return x

    def print_data(self):
        hash = self.get_original_hash()
        print(hash, len(hash))

    def print_working(self):
        hash = self.get_working_hash()
        print(hash, len(hash))

    def get_bitstring(self, unsigned long bits):
        cdef int i
        cdef unsigned long long o
        x = ""
        o = 1
        for i in range(sizeof(bits) * BITS_IN_CHAR):
            if o & bits:
                x = "1" + x
            else:
                x = "0" + x
            o <<= 1
        return x

    def print_bitstring(self, unsigned long long bits):
        print(self.get_bitstring(bits))

    def __richcmp__(Hash self, Hash other, int op):
        if op == 0:
            return self.working < other.working
        return 0

