from game import *

# Keyboard listeners for the game (WINDOWS ONLY)
import msvcrt


class UI2048:
    """ Provides a very simple UI for the game 2048

        Uses Board2048 as the game board, together with operations on that.
        Also uses Windows-specific keyboard listeners.
    """
    def __init__(self, board=None):
        if board is None:
            self.board = Board2048()
        else:
            self.board = board

    """ Listens for a keystroke (Windows-specific)

        Based off of
        http://stackoverflow.com/questions/11918999/key-listeners-in-python
    """
    @staticmethod
    def _kbfunc():
        # this is boolean for whether the keyboard has been hit
        x = msvcrt.kbhit()
        if x:
            # getch acquires the character encoded in binary ASCII
            ret = msvcrt.getch()
        else:
            ret = False
        return ret

    """ Runs the UI.

        Listens for keystrokes, then performs the following actions:
        ASDW -> move keystrokes
        SPACEBAR -> quit game (prints out score, # of turns passed)
        Z -> print out score, # of turns passed
    """
    def run(self):
        print(str(self.board))
        # infinite loop, which runs until SPACEBAR is pressed
        while True:

            # acquire the keyboard hit if exists
            evt = UI2048._kbfunc()

            # if we got a keyboard hit
            if evt:
                ch = evt.decode()
                if ch == 'd':
                    # key is d; move right
                    self.board.move(0)
                    print(str(self.board))
                elif ch == 'w':
                    # key is w; move up
                    self.board.move(1)
                    print(str(self.board))
                elif ch == 'a':
                    # key is a; move left
                    self.board.move(2)
                    print(str(self.board))
                elif ch == 's':
                    # key is s; move down
                    self.board.move(3)
                    print(str(self.board))
                elif ch == ' ':
                    # key is spacebar; stop game
                    print(str(self.board))
                    print("Your score is: " + str(self.board.score))
                    print("Turn number: " + str(self.board.num_steps))
                    break
                elif ch == 'z':
                    # print score
                    print("Your score is: " + str(self.board.score))
                    print("Turn number: " + str(self.board.num_steps))
