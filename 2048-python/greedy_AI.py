from game import *


class GreedyAI:
    """ A greedy algorithm that tries to optimize score

        b is a Board2048 object that the AI will try to solve
        iter is the number of turns the AI looks into the future
        This AI is very simple, it will try to maximize score over a fixed
        number of turns, without taking any other factors into account.
        It also does not take random spawns into account
    """
    def __init__(self, b=None, iter=1, s=None):
        if b is None:
            self.board = Board2048(seed=s)
        else:
            self.board = b
        self.iters = iter

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

        Returns the move that the AI made, or -1 if the game was over.
        If AI's move wasn't possible, tries to move in the following order:
        right, then up, then left, then down
    """
    def move(self):
        # game is over; do nothing
        if(self.board.game_over()):
            return -1
        # calculate AI's move
        dir = GreedyAI._calc_move(self.board, self.iters)[1]
        # try to move in that direction
        if(self.board.move(dir)):
            return dir
        # if the move failed, try all possible moves in order
        for dir in gs:
            if(self.board.move(dir)):
                return dir
        # should never happen
        raise RuntimeError("ERROR: No moves possible, but game not over")
