from py3dbp.main import *

if __name__ == '__main__':
    bin = Bin("1", 100, 100, 100)
    item1 = Item("1", 100, 100, 10, False)
    item2 = Item("2", 10, 100, 100, False)
    bins = pack(100, 100, 100, [item1, item2])
    print(bins)
