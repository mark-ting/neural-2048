# -*- coding: utf-8 -*-

from neural_network import NeuralNetwork as N
from game import *
from heuristics import Heuristics as H
from parse_game import *

class NeuralAI:
    def __init__(self, weight_matrix=None, b=None, s=None):

        self.network = N(16, 4, 8, 2)

        if b is None:
            self.board = Board2048(seed=s)
        else:
            self.board = b

    def move(self):
        # game is over; do nothing
        if(self.board.game_over()):
            return -1
        # calculate AI's move
        out = self.network.propogate(parse_pair((self.board, 0))[0])
        dir = H.max_val(out)
        # try to move in that direction
        if(self.board.move(dir)):
            return dir
        # if the move failed, try all possible moves in order
        for dir in gs:
            if(self.board.move(dir)):
                return dir
        # should never happen
        raise RuntimeError("ERROR: No moves possible, but game not over")
