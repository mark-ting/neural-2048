# -*- coding: utf-8 -*-
""" Contains methods designed to work in tandem with Object2048 in order to
    evalu using numpy library functions.
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

    """ Exposes values of 2048 objects; must specify if input is a linear array
        or 2D array
    """
    def expose_val(array):
        def f(x): return x.val
        f = np.vectorize(f)
        return f(array)
        #return list([x.val for x in array])

    """ Verifies array is in ascending order (left -> right, up -> down) """
    def ascending(array):
        for i in range(len(array) - 1):
            if array[i] > array[i+1]:
                return False
        return True
            #for x, value in np.ndenumerate(array):

    """ Verifies array is in descending order (left -> right, up -> down).
        Identical numbers are accepted (0, 2, 2, 4 okay)
    """
    def descending(array):
        for i in range(len(array) - 1):
            if array[i] < array[i+1]:
                return False
        return True

    """ Returns coordinates of the largest number (object) is on the board as a
        (0-indexed) tuple (x, y)
    """
    # PLACEHOLDER -- NEED TO RETURN THE COORDINATES NOT THE NUMBER
    def max_val(array):
        return np.amax(array)

    """ Returns number in a corner (starting from top-left and moving clockwise
        from 0-3 (TL: 0; TR: 1; BR: 2; BL: 3). Default to top left corner.
    """
    def corner(board2048, corner=0):
        grid = board2048.grid
        max_dim = np.shape(grid)
        X = max_dim[0] - 1
        Y = max_dim[1] - 1

        if corner == 0:
            corner_obj = (grid[0,0])

        elif corner == 1:
            corner_obj = (grid[X, 0])

        elif corner == 2:
            corner_obj = (grid[X, Y])

        elif corner ==3:
            corner_obj = (grid[0, Y])

        return corner_obj.val