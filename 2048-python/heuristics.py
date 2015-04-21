# -*- coding: utf-8 -*-
""" Contains methods designed to work in tandem with 2048 Game in order to
    determine evident traits (heuristics) and validate game structure.
"""

import numpy as np
from game import Obj2048
from game import Board2048

""" test object/board setup -- pulled from test.py """
t = Obj2048(2)
f = Obj2048(4)
e = Obj2048(8)
s = Obj2048(16)
x = Board2048(np.array([[f, t, s, t], [t, e, t, f],
                        [e, t, f, t], [t, e, t, f]]))


class Heuristics:
    def extract_val(numpy_array):
        list(map(lambda e: e.val, numpy_array))

    """ verifies that an array is of ascending value (left -> right) """
    def ascending(array):
        for x, value in numpy.ndenumerate(array):
            tempvar = x

        return False

    """ verifies that an array is of descending value (left -> right) """
    def descending(array):
        return False

def main():
    """ Extract rows and columns from numpy grid"""
    nrow1 = x.grid[0, :]
    nrow2 = x.grid[1, :]
    nrow3 = x.grid[2, :]
    nrow4 = x.grid[3, :]
    ncol1 = x.grid[:, 0]
    ncol2 = x.grid[:, 1]
    ncol3 = x.grid[:, 2]
    ncol4 = x.grid[:, 3]

    row1 = extract(nrow1)
    row2 = extract(nrow2)
    row3 = extract(nrow3)
    row4 = extract(nrow4)
    col1 = extract(ncol1)
    col2 = extract(ncol2)
    col3 = extract(ncol3)
    col4 = extract(ncol4)

    print(row1)

    print("TESTING HEURISTICS!")
