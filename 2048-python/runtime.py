import argparse

from game import *
from greedy_AI import *

# command line argument intake for runtime options
parser = argparse.ArgumentParser( \
    description="Run 2048 with an AI", \
    epilog="Default option is 1")
    
parser.add_argument('--ai', help="1: Greedy | 2: Novice | 3: Expert", \
    default=1, type=int)
    
#parser.add_argument('--ui', help="Run the game in a terminal UI")

args = parser.parse_args()
mode = args.ai

if mode == 1:
    print("Search depth set to 3")
    search_depth = 3
elif mode == 2:
    print("Search depth set to 5")
    search_depth = 5
elif mode == 3:
    print("Search depth set to 10")
    search_depth = 10
elif mode == 4:
    import UI.py

if mode != 4:
    g = Grid2048()
    ai_player = GreedyAI(g, search_depth)    

    print("WORK IN PROGRESS!")
"""
    while True:    
        next_move = (ai_player.calc_move(search_depth))[2]
        g.move(next_move)    
"""
#class NoviceRuntime: