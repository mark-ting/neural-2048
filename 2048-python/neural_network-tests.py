import numpy as np
from game import Obj2048
from game import Board2048
from heuristics import Heuristics as hu
from neural_network import NeuralNetwork as N
from propagation_functions import tanh, tanh_prime, expit, expit_prime

ALG_SET1 = (tanh, tanh_prime)
ALG_SET2 = (expit, expit_prime)

I = [1, 1, 0, 0, 0, 0, 0, 1]  # input set

W = [[1, 1, 1, 1, 1, 1, 1, 1],  # input layer
     [2, 1, 2, 2],  # hidden layer 1
     [3, 3, 4, 3],  # hidden layer 2
     [1, 1, 2, 7]]        # output layer

BW = [[0,0], [0], [1, 2, 3, 2]]  # BAD WEIGHT MATRIX; USE TO BREAK THINGS.

N_IN = 8
N_OUT = 4
N_HIDDEN = 4
N_LAYERS = 2

#T_DATA = [input_, output_]
L_RATE = 0.5
E_BOUND = 0.000001

network = N(N_IN, N_OUT, N_HIDDEN, N_LAYERS, ALG_SET2)

print(str(network.total_layers - 1))
print(str(network.weights))

network.load_weights(W)

print("weights loaded...")

network.propogate(I)


""" THESE CAN AND SHOULD CAUSE ASSERTION ERRORS. """
#network.load_weights(BW)