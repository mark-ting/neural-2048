from game import *

class GreedyAI:
    ## b is a Board2048 object that the AI will try to solve
    ## iter is the number of turns the AI looks into the future
    ## this AI is very simple, it will try to maximize score
    ## it also does not take random spawns into account
    def __init__(self, b=None, iter=1):
        if b == None:
            self.board = Board2048()
        else:
            self.board = g
        self.iters = iter

    ## computes all future outcomes up to a certain depth,
    ## then returns a tuple consisting of a list of all board outcomes,
    ## plus the direction of motion yielding the maximum score across all outcomes
    ## does not take random spawns into account
    @staticmethod
    def calc_move(board, iter):
        if iter == 0:
            return ([board], 0)
        board_arr = []
        # maximum score attainable, together with the direction to move in
        dir = (-1, 0)
        for i in gs:
            # make new Board2048 object so we don't change original copy
            new_board = Board2048(Board2048.copy_grid(board.grid))
            # move it in the given direction
            new_board.move_without_spawn(i)
            # get tree of moves one level down
            sub_board_arr = GreedyAI.calc_move(new_board)[0]
            # get scores (we maximize this)
            scores = list(map(lambda b: b.score, sub_board_arr))
            max_s = max(scores)
            if(max_s > dir[0]):
                dir = (max_s, i)
            board_arr.append(sub_board_arr)
        return (board_arr, dir[1])
            
    ## moves current instance
    ## returns true if AI's move was possible
    ## if AI's move wasn't possible, tries to move in the following order:
    ## right, then up, then left, then down
    def move(self):
        # game is over; do nothing
        if(self.board.game_over()):
            return False
        # calculate AI's move
        dir = calc_move(self.board, self.iters)[1]
        # try to move in that direction
        if(self.board.move(dir)):
            return True
        # if the move failed, try all possible moves in order
        for dir in gs:
            if(self.board.move(dir)):
                return False
        # should never happen
        raise RuntimeError("ERROR: No moves possible, but game not over")