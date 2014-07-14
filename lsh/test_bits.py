import random
import pyximport; pyximport.install()
from lsh import bits


if __name__ == "__main__":
    h = bits.Hash([True if i < 3 else False for i in range(128)])
    print(bits.NBITS())
    h.print_data()
    h.print_working()
    print(bin(h.get_prefix(5)))
    h.lrotate(65)
    h.print_data()
    h.print_working()
    print(bin(h.get_prefix(5)))
    h.shuffle([random.randint(i, 127) for i in range(128)])
    h.print_working()
