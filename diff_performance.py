from timeit import timeit
from itertools import product

from diff_functions import diff_functions, diff2_functions

def time_functions():
    core = open('core.txt').read().split()
    print("*** diff functions ***")
    for diff in diff_functions:
        stmt = 'for inputs in product(core[:200], repeat=2): diff(*inputs)'
        locals = {"diff": diff, "core": core}
        print(diff.__name__, timeit(stmt, globals=dict(**globals(), **locals),number=10))
    print("*** diff2 functions ***")
    for diff2 in diff2_functions:
        stmt = 'for inputs in product(core[:50], repeat=3): diff2(*inputs)'
        locals = {"diff2": diff2, "core": core}
        print(diff2.__name__, timeit(stmt, globals=dict(**globals(), **locals),number=10))

if __name__ == '__main__':
    time_functions()
    # print(diff_n("toxic", ["train", "taper"]))
