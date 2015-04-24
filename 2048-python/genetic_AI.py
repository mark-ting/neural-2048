from game import *
import random as rand

class GeneticAI:
    # Determines how fast we hone in on the solution
    lambda_change_factor = 0.999
    def __init__(self, b=None, row_arr=None, col_arr = None, s=None):
        if b is None:
            self.board = Board2048(seed=s)
        else:
            self.board = b
        if row_arr is None:
            self.row_arr = DeepAI.rand_array()
        else:
            self.row_arr = row_arr
        if col_arr is None:
            self.col_arr = DeepAI.rand_array()
        else:
            self.col_arr = col_arr
        self.best_row_arr = row_arr
        self.best_col_arr = col_arr
        self.best_score = 0
        self.lambda = 1.0

    @staticmethod
    def rand_array():
        arr = np.zeros(num_rc)
        for i in gs:
            arr[i] = rand.random() * 2 - 1
        return arr
        
    @staticmethod
    def calc_move():
        dir_f = np.dot(np.dot(self.col_arr, self.board.grid), self.row_arr)
        # normalize so that we don't always go down later in the game
        dir_f /= np.sum(self.board.grid)
        if dir_f <= 0:
            return 0
        if dir_f >= 3:
            return 3
        else:
            return round(dir_f)
        
    """ Moves the board according to the genetic AI's algorithm.

        Returns the move that the AI made, or -1 if the game was over.
        If AI's move wasn't possible, tries to move in the following order:
        right, then up, then left, then down
    """
    def move(self):
        # game is over; do nothing
        if(self.board.game_over()):
            return -1
        # calculate AI's move
        dir = GeneticAI._calc_move(self.board, self.iters)[1]
        # try to move in that direction
        if(self.board.move(dir)):
            return dir
        # if the move failed, try all possible moves in order
        for dir in gs:
            if(self.board.move(dir)):
                return dir
        # should never happen
        raise RuntimeError("ERROR: No moves possible, but game not over")
    
    """ Plays an entire game, until it loses; returns the score """
    def play(self):
        while self.move() != -1:
            # do nothing
        return self.board.score

    def train(self, num_games):
        for i in range(num_games):
            score = self.play()
            if score > self.best_score:
                self.best_score = score
                self.best_row_arr = self.row_arr
                self.best_col_arr = self.col_arr
            self.row_arr = self.best_row_arr + lambda * rand_array()
            self.col_arr = self.best_col_arr + lambda * rand_array()
            lambda *= lambda_change_factor