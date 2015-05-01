""" This file holds a collection of possibly useful testing code. """
from game import *
from greedy_AI import *
import numpy as np
from genetic_AI import *
from parse_game import *

#for i in range(10):
    #print(parse_char(str(i)))

#for i in range(ord('a'), ord('f') + 1):
    #print(parse_char(chr(i)))

s = "0123\n4567\n89ab\ncdef\naasdfasdfasf"
#print(str(parse_nbyn(s)))
board = Board2048()
print(board.grid)
print(board.grid[0][0])

datafile="C:\\Users\\Adam\\Dropbox\\Spring2015\\CS_51\\2048-heuristic-ai\\2048-ai-master\\training_data\\Output_1.txt"
#print(parse_move("Move #2, move chosen down, current score=0"))
x = load_datafile(datafile)
for i in range(len(x)):
    print(type(x[i][0].grid[0][0].val))

"""
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
"""

""" Some testing code, which demonstrates RNG seeding """

"""
ai = GeneticAI()
ai.train(10000)
while(not ai.board.game_over()):
    print(ai.board)
    ai.move()
print(ai.board)
print("Score = " + str(ai.board.score))
"""

#ui = UI2048(x)
#ui.run()
