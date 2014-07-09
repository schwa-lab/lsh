"""
Simple hash container with a basic bitwise left rotate operation
"""


DEF BITS_IN_CHAR = 4

cdef class Hash:
    cdef unsigned long data # 128 bit

    def __cinit__(self, data):
        self.data = data

    def lrotate(self, unsigned int shift):
        self.data = (self.data << shift) | (self.data >> (sizeof(self.data) * BITS_IN_CHAR - shift))

    def rrotate(self, unsigned int shift):
        """Doesn't seem to work :("""
        self.data = (self.data >> shift) | (self.data << (sizeof(self.data) * BITS_IN_CHAR - shift))

    def get_data(self):
        return self.data

    def get_prefix(self, unsigned int length):
        return self.data >> (sizeof(self.data) - length)

    def __richcmp__(Hash self, Hash other, int op):
        if op == 0:
            return self.data < other.data
        return 0

