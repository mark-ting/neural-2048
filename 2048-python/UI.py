from game import *

# Keyboard listeners for the game (WINDOWS ONLY)
import msvcrt
import time

board = Board2048()
print(str(board))

"""
    
    The following key-listener code is based off of
    http://stackoverflow.com/questions/11918999/key-listeners-in-python
    
"""

# asks whether a key has been acquired
def kbfunc():
    #this is boolean for whether the keyboard has bene hit
    x = msvcrt.kbhit()
    if x:
        #getch acquires the character encoded in binary ASCII
        ret = msvcrt.getch()
    else:
        ret = False
    return ret

#infinite loop
while True:

    #acquire the keyboard hit if exists
    evt = kbfunc() 

    #if we got a keyboard hit
    if evt != False:
        ch = evt.decode()
        if ch == 'd':
            # key is d; move right
            board.move(0)
            print(str(board))
        elif ch == 'w':
            # key is w; move up
            board.move(1)
            print(str(board))
        elif ch == 'a':
            # key is a; move left
            board.move(2)
            print(str(board))
        elif ch == 's':
            # key is s; move down
            board.move(3)
            print(str(board))
        elif ch == ' ':
            # key is spacebar; stop game
            print(str(board))
            print("Your score is: " + str(board.score))
            break
        elif ch == 'z':
            # print score
            print("Your score is: " + str(board.score))