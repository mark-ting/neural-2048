from game import *
import random as rand

class GeneticAI:
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

    @staticmethod
    def rand_array():
        arr = np.zeros(num_rc)
        for i in gs:
            arr[i] = rand.random() * 2 - 1
        return arr
        
    def move():
        dir_f = 
        
    def train(num_games):
        
    """ Computes all future outcomes up to a certain depth

        Returns a tuple consisting of a list of all board outcomes,
        plus the direction of motion yielding the maximum score across all
        outcomes. Does not take random spawns into account
    """
    @staticmethod
    def _calc_move(board, iter):
        if iter == 0:
            return ([board], 0)
        board_arr = []
        # maximum score attainable, together with the direction to move in
        dir = (-1, 0)
        for i in gs:
            # make new Board2048 object so we don't change original copy
            new_board = Board2048(np.copy(board.grid))
            # move it in the given direction
            new_board.move_without_spawn(i)
            # get tree of moves one level down
            sub_board_arr = GreedyAI._calc_move(new_board, iter - 1)[0]
            # get scores (we maximize this)
            scores = list(map(lambda b: b.score, sub_board_arr))
            max_s = max(scores)
            if(max_s > dir[0]):
                dir = (max_s, i)
            board_arr += sub_board_arr
        return (board_arr, dir[1])

    """ Moves the board according to the greedy AI's algorithm.

        Returns true if AI's move was possible
        If AI's move wasn't possible, tries to move in the following order:
        right, then up, then left, then down
    """
    def move(self):
        # game is over; do nothing
        if(self.board.game_over()):
            return False
        # calculate AI's move
        dir = GreedyAI._calc_move(self.board, self.iters)[1]
        # try to move in that direction
        if(self.board.move(dir)):
            return True
        # if the move failed, try all possible moves in order
        for dir in gs:
            if(self.board.move(dir)):
                return False
        # should never happen
        raise RuntimeError("ERROR: No moves possible, but game not over")
