import pyximport; pyximport.install()
from lsh import bits


if __name__ == "__main__":
    h = bits.Hash(0)
    h.lrotate(1)
    print(h.get_data())
    h.rrotate(1)
    print(h.get_data())

    h = bits.Hash(1)
    h.lrotate(1)
    print(h.get_data())
    h.lrotate(1)
    print(h.get_data())
    h.lrotate(1)
    print(h.get_data())
    h.rrotate(1)
    print(h.get_data())
