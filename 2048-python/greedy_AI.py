from game import *

class GreedyAI:
    ## g is a Grid2048 object that the AI will try to solve
    ## i is the number of turns the AI looks into the future
    ## this AI is very simple, it will try to maximize score
    ## it also does not take random spawns into account
    def __init__(self, g=None, iter=1):
        if g == None:
            self.grid = Grid2048()
        else:
            self.grid = g
        self.iters = iter

    ## computes all future outcomes up to a certain depth,
    ## then returns a tuple consisting of a list of all outcomes,
    ## plus the direction of motion yielding the maximum score across all outcomes
    ## does not take random spawns into account
    ## here g is a Grid2048, not an actual grid/matrix
    def calc_move(g, iter):
        if iter == 0:
            return ([g], 0)
        grid_arr = []
        # maximum score attainable, together with the direction to move in
        dir = (-1, 0)
        for i in gs:
            # copy grid so we don't change the original copy
            new_grid = g.copy_grid(g.grid)
            # make new Grid2048 object
            new_g = Grid2048(new_grid)
            # move it in the given direction
            new_g.move_without_spawn(i)
            # get tree of moves one level down
            grids = calc_move(new_g)[0]
            # get scores (we maximize this)
            scores = list(map(lambda g: g.score, grids))
            max_s = max(scores)
            if(max_s > dir[0]):
                dir = (max_s, i)
            grid_arr.append(grids)
        return (grid_arr, dir[1])     