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

    def expose_val(array):
        """ Exposes values of 2048 objects. """
        def f(x): return x.val
        f = np.vectorize(f)
        return f(array)

    def ascending(array):
        """ Verifies array is in ascending order.

            Horizontal arrays: left -> right
            Vertical arrays: top -> bottom

            Identical adjacent numbers are acceptable: [0, 2, 2, 4] is OK
        """
        for i in range(len(array) - 1):
            if array[i] > array[i+1]:
                return False
        return True
        # for x, value in np.ndenumerate(array):

    def descending(array):
        """ Verify array is in descending order.

            Horizontal arrays: left -> right
            Vertical arrays: top -> bottom

            Identical adjacent numbers are acceptable: [4, 2, 2, 0] is OK
        """

        for i in range(len(array) - 1):
            if array[i] < array[i+1]:
                return False
        return True

    # PLACEHOLDER -- NEED TO RETURN THE COORDINATES NOT THE NUMBER
    def max_val(array):
        """ Return the value of the largest (object) on the board.

            DOES NOT YET:
            location...in the form of a zero-indexed tuple (x, y)
        """
        return np.amax(array)


    def corner(board2048, corner=0):
        """ Return the value of the corner object on a 2048 board.

            Args:
                board2048 (Object2048): game board to analyze
                corner (int): specifies which corner to look in
                  0 -- Top-Left
                  1 -- Top-Right
                  2 -- Bottom-Right
                  3 -- Bottom-Left
                  (Defaults to top left corner if nothing is specified)

        """

        grid = board2048.grid
        max_dim = np.shape(grid)
        X = max_dim[0] - 1  # right-most coordinate
        Y = max_dim[1] - 1  # upper-most coordinate

        if corner == 0:
            corner_obj = (grid[0, 0])  # Top-Left

        elif corner == 1:
            corner_obj = (grid[X, 0])  # Top-Right

        elif corner == 2:
            corner_obj = (grid[X, Y])  # Bottom-Right

        elif corner == 3:
            corner_obj = (grid[0, Y])  # Bottom-Left

        return corner_obj
