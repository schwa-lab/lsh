#!/usr/bin/env python3

class LSHItem(object):
    __slots__ = ('id', 'signature', 'count', 'vector', 'bow')
    def __init__(self, id, signature, count=0, vector=None, bow=None):
        self.id = id
        self.signature = signature
        self.count = count
        if vector is None:
            self.vector = []
        else:
            self.vector = vector

        if bow is None:
            self.bow = []
        else:
            self.bow = bow

    def __str__(self):
        return '{} {}'.format(self.id, self.signature)

    
    def __repr__(self):
        return str(self)


    def __hash__(self):
        return hash(self.id)
