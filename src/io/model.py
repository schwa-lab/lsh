#!/usr/bin/env python3
import struct

class LSHItem(object):
    def __init__(self, id, signature, count=0, vector=None):
        self.id = id
        self.signature = signature
        self.count = count
        if vector is None:
            self.vector = []
        else:
            self.vector = vector

    def __str__(self):
        return '{} {}'.format(self.id, self.signature)
