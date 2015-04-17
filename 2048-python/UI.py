from game import *

# Keyboard listeners for the game (WINDOWS ONLY)
import msvcrt
import time

g = Grid2048()
print(str(g))
print(num_rc)

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
    x = kbfunc() 

    #if we got a keyboard hit
    if x != False:
        y = x.decode()
        if y == 'd':
            # key is d; move right
            g.move(0)
            print(str(g))
        elif y == 'w':
            # key is w; move up
            g.move(1)
            print(str(g))
        elif y == 'a':
            # key is a; move left
            g.move(2)
            print(str(g))
        elif y == 's':
            # key is s; move down
            g.move(3)
            print(str(g))
        elif y == ' ':
            # key is spacebar; stop game
            print(str(g))
            print("Your score is: " + str(g.score))
            break
        elif y == 'z':
            # print score
            print("Your score is: " + str(g.score))