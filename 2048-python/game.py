# Other utilities
import numpy as np
import random as rand

""" Number of rows and columns in grid """
num_rc = 4
""" Grid size; convenient for 'for' loops """
gs = range(num_rc)


""" Implements a 2048 object (for now, just ints) """
class Obj2048:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

""" Implements a 2048 board, supports variable object types """
class Board2048:

    """ Initializes the board.

        The board has the following values:
        score: represents the score
        num_steps: how many (successful) moves have been made
        grid: The grid for 2048.
            Implemented as a Numpy array of Obj2048's.
            This means you'll have to use .val to compare elements directly.
            Can be initialized as a specific grid, if none is provided then
            it will be initialized with two 2's in random positions.

        NOTES:
            - Random number generator: all instances of Board2048, and of all
                classes in general, share THE SAME random number generator.
                This is usually not a problem, but when trying to seed the RNG
                you have to be careful. If you seed any RNG, you'll seed all of
                them. Thus, if having a reproducible sequence of grids for a
                particular Board2048 is important, it is strongly advisable to
                seed only that Board2048 object, and not seed any others.
                Board2048s that aren't seeded will not change the RNG.


            - Use method game_over() instead of variable _gameOver

        CONVENTIONS:
            - The "grid" is the Numpy matrix.
            - A "location" is a tuple (x, y) of coordinates on the grid.

        LIST OF METHODS, with brief descriptions
            (for more detailed descriptions see the individual methods):
            __init__: initializes board
            __str__: called as str(board) - gives string representation of
                matrix, calling Obj2048's __str__ method along the way.
            get_empty_locs: returns the list of empty locations in grid
            get_adjacent_loc: gets adjacent location from a given location in
                a given direction. Static.
            can_move: checks if a move in a given direction is possible
            move_without_spawn: moves the grid, doesn't spawn a new number
            move: moves the grid, spawns a new number
            game_over: checks if the game is over (i.e. no possible moves)
            print_game_over_message: prints a message with some info about the
                game (intended to be printed when the game is over).
    """
    def __init__(self, grid=None, seed=None):
        self.num_steps = 0
        self._gameOver = False
        self.score = 0
        if seed is not None:
            rand.seed(seed)
        if grid is None:
            self.grid = np.full((num_rc, num_rc), Obj2048(0), dtype=Obj2048)
            self._spawn_rand()
            self._spawn_rand()
        else:
            # Copy grid over, so as to not have interference between two boards
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

    """ Gets empty locations on grid

        Returns their coordinates as a list of tuples,
        e.g. if (0, 0) and (1, 2) are the only empty spaces,
        then [(0, 0), (1, 2)] is returned
    """
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
    def _spawn_rand(self):
        empty = self.get_empty_locs()
        l = len(empty)  # Assuming l != 0; this case should be covered in move
        pos = empty[rand.randrange(0, l)]
        self.grid[pos[0]][pos[1]] = Obj2048(2)

    """ Gets location adjacent to (x, y) in direction dir

        0 = right, 1 = up, 2 = left, 3 = down
    """
    @staticmethod
    def get_adjacent_loc(loc, dir):
        x = loc[0]
        y = loc[1]
        if dir == 0:
            new_loc = (x, y + 1)
        elif dir == 1:
            new_loc = (x - 1, y)
        elif dir == 2:
            new_loc = (x, y - 1)
        elif dir == 3:
            new_loc = (x + 1, y)
        else:
            raise ValueError("direction can only be 0, 1, 2, or 3")
        if (0 <= new_loc[0] < num_rc and 0 <= new_loc[1] < num_rc):
            return new_loc
        else:
            return None

    """ Checks if a move in a given direction is possible """
    def can_move(self, dir):
        for i in gs:
            for j in gs:
                loc = Board2048.get_adjacent_loc((i, j), dir)
                if loc is None:
                    continue
                if (self.grid[i][j] != 0 and
                    ((self.grid[i][j].val == self.grid[loc[0]][loc[1]].val) or
                        self.grid[loc[0]][loc[1]].val == 0)):
                    return True
        return False

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

    """ Shifts all numbers on board in a direction, but does not merge them """
    def _shift(self, dir):
        for step in gs:
            for i in gs:
                for j in gs:
                    loc = Board2048.get_adjacent_loc((i, j), dir)
                    if loc is None:
                        continue
                    num = self.grid[loc[0]][loc[1]]
                    if num.val == 0:
                        self.grid[loc[0]][loc[1]] = self.grid[i][j]
                        self.grid[i][j] = Obj2048(0)

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
                self._merge_arr(self.grid[:, i])
            elif (dir == 2):
                self._merge_arr(self.grid[i])
            elif (dir == 3):
                self._merge_arr(self.grid[:, i][::-1])

        self._shift(dir)
        return True

    """ Moves entire grid one unit in direction dir.

        Returns whether or not the move was successful
        (i.e. pieces actually moved)
    """
    def move(self, dir):
        if (self.move_without_spawn(dir)):
            self._spawn_rand()
            self.num_steps += 1
            return True
        else:
            return False

    """ Checks if game is over """
    def game_over(self):
        if(self._gameOver):
            return True
        empty = self.get_empty_locs()
        l = len(empty)
        if (l == 0 and (not self.can_move(0) and (not self.can_move(1) and
                        (not self.can_move(2) and (not self.can_move(3)))))):
            self._gameOver = True
            return True
        return False

    """ Prints the game over message """
    def print_game_over_message(self):
        print("Game Over! Press SPACEBAR to exit.")
        print("Your score is: " + str(self.score))
        print("You lasted " + str(self.num_steps) + " steps!")
