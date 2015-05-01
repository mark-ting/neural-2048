from game import *
from math import log

""" Parses a hexadecimal character into an Obj2048 """
def parse_char(ch):
    # Char is a 0
    if ch == '0':
        return Obj2048(0)
    for i in range(ord('1'), ord('9') + 1):
        # Char is a number, between 2 and 512
        if ord(ch) == i:
            return Obj2048(2**(i - ord('1') + 1))
    for i in range(ord('a'), ord('f') + 1):
        # Char is a hexadecimal number
        if ord(ch) == i:
            return Obj2048(2**(i - ord('a') + 10))
    raise ValueError("ERROR: Character " + ch + " is an invalid hexadecimal number.")
    
""" Parses a nxn string matrix into a Board2048; assumes n = num_rc """
def parse_nbyn(s):
    # Initialize grid
    grid = np.full((num_rc, num_rc), Obj2048(0), dtype=Obj2048)
    count = 0
    for i in range(num_rc):
        for j in range(num_rc):
            grid[i][j] = parse_char(s[count])
            count += 1
        # skip newline
        count += 1
    return Board2048(grid)
    
""" Parses a move string with ... move chosen <MOVE> ... to the move number """
def parse_move(s):
    # find where the move is
    pos = s.find("move chosen ") + 12
    sub_s = ""
    # continue until we find the comma at the end of the move
    while s[pos] != ',':
        sub_s += s[pos]
        pos += 1
    if sub_s == "right":
        return 0
    elif sub_s == "up":
        return 1
    elif sub_s == "left":
        return 2
    elif sub_s == "down":
        return 3
    raise ValueError("ERROR: Invalid move")
    
""" Loads datafile into an array of tuples of Board2048's and moves

    Each tuple corresponds to a Board2048, together with the move
    the heuristic AI is about to make
"""
def load_datafile(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
        tuple_arr = []
        num_lines = len(data)
        # Don't want last matrix, since game is over
        curr_matrix = ""
        curr_board = None
        for i in range(num_lines - 7):
            if (i % 8 in range(4)):
                curr_matrix += data[i]
            elif (curr_matrix != ""):
                curr_board = parse_nbyn(curr_matrix)
                curr_matrix = ""
            if (i % 8 == 7):
                tuple_arr.append((curr_board, parse_move(data[i])))
        return tuple_arr
        
        
""" Parses a tuple array of (Board2048, move) pairs.

    Returns tuples of input/output neuron states, compatible with the neuron
    network.
"""
def parse_arr(tuple_arr):
    return list(map(parse_pair, tuple_arr))
    
    
""" Parses a tuple (Board2048, move) into input/output neuron states. """
def parse_pair(pair):
    neuron_arr = []
    sum = 0
    for i in gs:
        for j in gs:
            value = pair[0].grid[i][j].val
            if value != 0:
                sum += log(value, 2)
    for i in gs:
        for j in gs:
            value = pair[0].grid[i][j].val
            if value == 0:
                neuron_arr.append(0)
            else:
                neuron_arr.append(log(value, 2)/sum)
    if pair[1] == 0:
        return (neuron_arr, [0,0,0,1])
    elif pair[1] == 1:
        return (neuron_arr, [0,0,1,0])
    elif pair[1] == 2:
        return (neuron_arr, [0,1,0,0])
    elif pair[1] == 3:
        return (neuron_arr, [1,0,0,0])
    else:
        raise ValueError("ERROR: Move must be 0, 1, 2, or 3")