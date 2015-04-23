""" This file holds a collection of possibly useful testing code. """
from game import *
from greedy_AI import *
from UI import *
import numpy as np

z = Obj2048(0)
t = Obj2048(2)
f = Obj2048(4)
e = Obj2048(8)
s = Obj2048(16)
x = Board2048(np.array([[z, t, t, t], [z, z, z, z],
                        [z, z, z, z], [z, z, z, z]]))
print(x)
print(x.can_move(0))
#x.move(0)
#print(x)


""" Some testing code, which demonstrates RNG seeding """

"""
ai = GreedyAI(iter=2, s=1618)
while(not ai.board.game_over()):
    print(ai.board)
    ai.move()
print(ai.board)
print("Score = " + str(ai.board.score))

"""
ui = UI2048(x)
ui.run()
