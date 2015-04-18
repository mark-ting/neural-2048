# Other utilities
import numpy as np
import random as rand

""" Number of rows and columns """
num_rc = 4
""" Grid size """
gs = range(num_rc)

""" Implements a 2048 object (for now, just ints) """
class Obj2048:
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return str(self.val)
    
""" Implements a 2048 board """
class Board2048:    
    def __init__(self, grid=None, seed=None):
        self.num_steps = 0
        self.gameOver = False
        self.score = 0
        if seed != None:
            rand.seed(seed)
        if grid == None:
            self.grid = np.full((num_rc, num_rc), Obj2048(0), dtype=Obj2048)
            two1 = (rand.randrange(0,num_rc), rand.randrange(0,num_rc))
            two2 = (rand.randrange(0,num_rc), rand.randrange(0,num_rc))
            while two1 == two2:
                two2 = (rand.randrange(0,num_rc), rand.randrange(0,num_rc))
            self.grid[two1[0]][two1[1]] = Obj2048(2)
            self.grid[two2[0]][two2[1]] = Obj2048(2)
        else:
            # Copy grid over, so as to not have interference between two objects
            self.grid = np.copy(grid)
        
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

    """Gets empty locations on grid, returns them as a list of tuples"""
    def get_empty_locs(self):
        empty = []
        for i in gs:
            for j in gs:
                if self.grid[i][j].val == 0:
                    empty.append((i, j))
        return empty
    
    """ Spawns a number on the board
    
        Only spawns 2s as of now
    """
    def spawn_rand(self):
        empty = self.get_empty_locs()
        l = len(empty) # Assuming l != 0; this case should be covered in move
        pos = empty[rand.randrange(0, l)]
        self.grid[pos[0]][pos[1]] = Obj2048(2)
        
    """ Gets location adjacent to (x, y) in direction dir
    
        0 = right, 1 = up, 2 = left, 3 = down
    """
    @staticmethod
    def get_adjacent_loc(x, y, dir):
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
    
    """ Checks if a move in a given direction is possible"""
    def can_move(self, dir):
        for i in gs:
            for j in gs:
                loc = Board2048.get_adjacent_loc(i, j, dir)
                if loc == None:
                    continue
                if self.grid[i][j] != 0 and\
                        ((self.grid[i][j].val == self.grid[loc[0]][loc[1]].val) or\
                        self.grid[loc[0]][loc[1]].val == 0):
                    return True
        return False
        
    """ Checks if game is over """
    def game_over(self):
        if(self.gameOver):
            return True
        empty = self.get_empty_locs()
        l = len(empty)
        if (l == 0 and (not self.can_move(0) and (not self.can_move(1) and\
                (not self.can_move(2) and (not self.can_move(3)))))):
            self.gameOver = True
            return True
        return False
        
    """ Prints the game over message """
    def print_game_over_message(self):
        print("Game Over! Press SPACEBAR to exit.")
        print("Your score is: " + str(self.score))
        print("You lasted " + str(self.num_steps) + " steps!")
    
    """ Merges all duplicate elements in an array
        
        Merges according to the rules of 2048, and to the left.
        It's up to the implementing program to change this to move in
        an arbitrary direction.
        Assumes arr is an array of num_rc Obj2048's.
        Changes arr in-place. Also updates score.
    """
    def _merge_arr(self, arr):
        for i in range(num_rc - 1):
            if (arr[i].val != 0 and (arr[i].val == arr[i+1].val)):
                arr[i] = Obj2048(arr[i].val * 2)
                self.score += arr[i].val
                arr[i+1] = Obj2048(0)
        
    """ Moves board, but doesn't spawn a new number"""
    def move_without_spawn(self, dir):
        if (self.game_over()):
            self.print_game_over_message()
            return False
        if (not self.can_move(dir)):
            return False
        self._shift(dir)
        # iterate through all rows or columns, then merge each one
        for i in gs:
            # change which rows and columns to merge based on direction
            if (dir == 0):
                self._merge_arr(self.grid[i][::-1])
            elif (dir == 1):
                self._merge_arr(self.grid[:,i])
            elif (dir == 2):
                self._merge_arr(self.grid[i])
            elif (dir == 3):
                self._merge_arr(self.grid[:,i][::-1])
        
        self._shift(dir)
        return True
        
    """ Moves entire grid one unit in direction dir.
    
        Returns whether or not the move was successful 
        (i.e. pieces actually moved)
    """
    def move(self, dir):
        if (self.move_without_spawn(dir)):
            self.spawn_rand()
            self.num_steps += 1
            return True
        else:
            return False
        
    """ Shifts all numbers on board in a direction, but does not merge them """
    def _shift(self, dir):
        for step in gs:
            for i in gs:
                for j in gs:
                    loc = Board2048.get_adjacent_loc(i, j, dir)
                    if loc == None:
                        continue
                    num = self.grid[loc[0]][loc[1]]
                    if num.val == 0:
                        self.grid[loc[0]][loc[1]] = self.grid[i][j]
                        self.grid[i][j] = Obj2048(0)