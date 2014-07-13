import pyximport; pyximport.install()
from lsh import bits


if __name__ == "__main__":
    h = bits.Hash([True if i < 3 else False for i in range(64)])
    h.print_data()
    h.print_working()
    print(bin(h.get_prefix(5)))
    h.lrotate(1)
    h.print_data()
    h.print_working()
    print(bin(h.get_prefix(5)))
