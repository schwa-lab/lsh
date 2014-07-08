#a!/usr/bin/env python3
from .model import LSHItem
from bitstring import BitArray
import pyximport; pyximport.install()
import bits
import random



class LSHReader:
    def __init__(self):
        pass

    def process_file(self, filelike):
        for line in filelike:
            yield self.process_line(line.strip())

    def process_line(self, line):
        line = line.split(' ')
        assert len(line) == 2, '{} does not match expected format of space limited line'.format(line)
        id, signature = line
        id = int(id)
        b_signature = BitArray('0b' + signature)
        n = 32
        splits = [b_signature[i:i+n].uint for i in range(0,len(b_signature),n)]
        signature = bits.Hash(splits)
        
        item = LSHItem(id, b_signature)
        return item

class BinaryReader:
    def __init__(self):
        pass


    def process_file(self, filelike):
        while True:
            id, sig = filelike.read(4), filelike.read(16)
            if not len(id) or not len(sig):
                break
            else:
                yield LSHItem(int(id), BitArray(sig))



if __name__ == '__main__':
    r = LSHReader()
    import sys
    for item in r.process_file(open(sys.argv[1], 'r')):
        print(item)
