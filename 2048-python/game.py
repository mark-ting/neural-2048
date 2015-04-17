# Other utilities
import numpy as np
import random as rand

# number of rows and columns
num_rc = 4
# grid size
gs = range(num_rc)

class Obj2048:
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return str(self.val)
    
class Grid2048:
    def make_zero_grid(self):
        grid = []
        for i in gs:
            temp_list = []
            for j in gs:
                temp_list.append(Obj2048(0))
            grid.append(temp_list)
        return grid
        
    ## copies g into a new grid
    ## since these are 2D lists, we need to use this rather than just x.copy()
    ## otherwise changing elements of new grid will overwrite old grid
    def copy_grid(self, g):
        grid = []
        for i in gs:
            grid.append(list(g[i]))
        return grid
    
    def __init__(self, g=None):
        if g == None:
            self.grid = self.make_zero_grid()
            two1 = (rand.randrange(0,num_rc), rand.randrange(0,num_rc))
            two2 = (rand.randrange(0,num_rc), rand.randrange(0,num_rc))
            while two1 == two2:
                two2 = (rand.randrange(0,num_rc), rand.randrange(0,num_rc))
            self.grid[two1[0]][two1[1]] = Obj2048(2)
            self.grid[two2[0]][two2[1]] = Obj2048(2)
        else:
            # Copy grid over, so as to not have interference between two objects
            self.grid = self.copy_grid(g)
        self.gameOver = False
        self.score = 0
        
    def __str__(self):
        ret_s = ""
        for i in gs:
            s = ""
            for j in gs:
                s += str(self.grid[i][j])
                if (j < num_rc - 1):
                    s += "    "
            ret_s += s + "\n"
        return ret_s

    def get_empty_locs(self):
        empty = []
        for i in gs:
            for j in gs:
                if self.grid[i][j].val == 0:
                    empty.append((i, j))
        return empty
    
    def spawn_rand(self):
        empty = self.get_empty_locs()
        l = len(empty) # Assuming l != 0; this case should be covered in move
        pos = empty[rand.randrange(0, l)]
        self.grid[pos[0]][pos[1]] = Obj2048(2)
        
    ## Gets location adjacent to (x, y) in direction dir
    ## 0 = right, 1 = up, 2 = left, 3 = down
    def get_adjacent_loc(self, x, y, dir):
        loc = {
            0 : (x, y + 1),
            1 : (x - 1, y),
            2 : (x, y - 1),
            3 : (x + 1, y)
        }.get(dir, (-1, -1))
        if (0 <= loc[0] < num_rc and 0 <= loc[1] < num_rc):
            return loc
        else:
            return None
    
    def can_move(self, dir):
        for i in gs:
            for j in gs:
                loc = self.get_adjacent_loc(i, j, dir)
                if loc == None:
                    continue
                if self.grid[i][j] != 0 and\
                        ((self.grid[i][j].val == self.grid[loc[0]][loc[1]].val) or\
                        self.grid[loc[0]][loc[1]].val == 0):
                    return True
        return False
        
    def game_over(self):
        if(self.gameOver):
            print("Game Over! Press SPACEBAR to exit.")
            print("Your score is: " + str(self.score))
            return True
        empty = self.get_empty_locs()
        l = len(empty)
        if (l == 0 and (not self.can_move(0) and (not self.can_move(1) and\
                (not self.can_move(2) and (not self.can_move(3)))))):
            self.gameOver = True
            print("Game Over! Press SPACEBAR to exit.")
            print("Your score is: " + str(self.score))
            return True
        return False
        
    def move_without_spawn(self, dir):
        if (self.game_over()):
            return False
        if (not self.can_move(dir)):
            return False
        self.shift(dir)
        grid = self.copy_grid(self.grid)
        
        for i in gs:
            for j in gs:
                if self.grid[i][j] == 0:
                    continue
                num = self.grid[i][j]
                loc = self.get_adjacent_loc(i, j, dir);
                if loc == None:
                    continue
                new_num = self.grid[loc[0]][loc[1]];
                if new_num.val == num.val: # merge two numbers together, update score
                    grid[loc[0]][loc[1]] = Obj2048(num.val + new_num.val)
                    self.score += (num.val + new_num.val)
                    grid[i][j] = Obj2048(0)
                    
        self.grid = grid
        self.shift(dir)
        return True
        
    ##  Moves entire grid one unit in direction dir.
    ##  Returns whether or not the move was successful (i.e. pieces actually moved)
    def move(self, dir):
        if (self.move_without_spawn(dir)):
            self.spawn_rand()
            return True
        else:
            return False
        
    def shift(self, dir):
        for step in gs:
            for i in gs:
                for j in gs:
                    loc = self.get_adjacent_loc(i, j, dir)
                    if loc == None:
                        continue
                    num = self.grid[loc[0]][loc[1]]
                    if num.val == 0:
                        self.grid[loc[0]][loc[1]] = self.grid[i][j]
                        self.grid[i][j] = Obj2048(0)