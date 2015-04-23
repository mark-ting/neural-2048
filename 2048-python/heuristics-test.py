import numpy as np
from game import Obj2048
from game import Board2048
from heuristics import Heuristics as hu

""" test object/board setup -- pulled from test.py """
z = Obj2048(0)
t = Obj2048(2)
f = Obj2048(4)
e = Obj2048(8)
s = Obj2048(16)

WIN = Obj2048(2048)
EWIN = Obj2048(4096)

x = Board2048(np.array([[t, z, z, f], [z, t, f, e],
                        [e, f, t, z], [e, z, EWIN, WIN]]))

""" Extract rows and columns from numpy grid"""
grid = hu.expose_val(x.grid)
row1 = grid[0, :]
row2 = grid[1, :]
row3 = grid[2, :]
row4 = grid[3, :]
col1 = grid[:, 0]
col2 = grid[:, 1]
col3 = grid[:, 2]
col4 = grid[:, 3]

row1_ascending = hu.ascending(row1)
row1_descending = hu.descending(row1)

row2_ascending = hu.ascending(row2)
row2_descending = hu.descending(row2)

row3_ascending = hu.ascending(row3)
row3_descending = hu.descending(row3)

max_num = hu.max_val(grid)

print("TESTING HEURISTICS!")
print("Rows:")
print(row1)
print(row2)
print(row3)
print(row4)
print("-----")
print("Columns:")
print(col1)
print(col2)
print(col3)
print(col4)



print("Printing grid:")
print(grid)
