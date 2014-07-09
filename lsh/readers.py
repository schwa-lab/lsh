#a!/usr/bin/env python3
from lsh.model import LSHItem
from bitstring import BitArray
import pyximport; pyximport.install()
from lsh import bits
import random
from lsh import hashes



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
        #sig = int(signature[:32], base=2)
        #signature = bits.Hash(sig)
        signature = hashes.Hashes(signature)

        item = LSHItem(id, signature)
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
