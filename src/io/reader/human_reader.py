from ..model import LSHItem
from bitstring import BitArray

class LSHReader(object):
    def __init__(self):
        pass

    def process_document(self, filelike):
        for line in filelike:
            yield self.process_line(line.strip())

    def process_line(self, line):
        line = line.split(' ')
        assert len(line) == 2, '{} does not match expected format of space limited line'.format(line)
        id, signature = line
        id = int(id)
        b_signature = BitArray('0b' + signature)
        item = LSHItem(id, b_signature)
        return item

if __name__ == '__main__':
    r = LSHReader()
    import sys
    for item in r.process_document(open(sys.argv[1], 'r')):
        print(item)
