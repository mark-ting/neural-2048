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

BW = [[0,0], [0], [1]]

N_IN = 4
N_OUT = 2
N_HIDDEN = 4
N_LAYERS = 2

network = N(N_IN, N_OUT, N_HIDDEN, N_LAYERS)

print(str(network.total_layers - 1))
print(str(network.weights))

network.load_weights(W)
network.propogate(I)

print(str(W))
print(str(network.save_weights))

""" THESE CAN AND SHOULD CAUSE ASSERTION ERRORS. """
#network.load_weights(BW)