import numpy as np
from game import Obj2048
from game import Board2048
from heuristics import Heuristics as hu
from neural_network import NeuralNetwork as N

ALG_SET = []

I = [0.5, 0.5, 0.5, 0.5]  # input set

W = [[1, 1, 1, 1],  # input layer
     [2, 2, 2, 2],  # hidden layer 1
     [3, 3, 3, 3],  # hidden layer 2
     [4, 4]]        # output layer


N_IN = 4
N_OUT = 2
N_HIDDEN = 4
N_LAYERS = 2

network = N(N_IN, N_OUT, N_HIDDEN, N_LAYERS, ALG_SET)

network.load_weights(W)
network.propogate(I)