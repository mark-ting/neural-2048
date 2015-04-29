import numpy as np
from game import Obj2048
from game import Board2048
from heuristics import Heuristics as hu
from neural_network import NeuralNetwork as N
#from neural_network_new import NeuralNetwork as N2
from propagation_functions import tanh, tanh_prime, expit, expit_prime, \
                                  linear, linear_prime

ALG_SET0 = (linear, linear_prime)
ALG_SET1 = (tanh, tanh_prime)
ALG_SET2 = (expit, expit_prime)

I = [1, 1, 1, 1, 1, 1, 1, 1]  # input set
B = 3

ZERO = np.zeros(8)

W = [np.random.rand(4, 9),
     np.random.rand(4, 4),
     np.random.rand(4, 4),
     np.random.rand(4, 4)]

BW = [[0,0], [0], [1, 2, 3, 2]]  # BAD WEIGHT MATRIX; USE TO BREAK THINGS.

N_IN = 8
N_OUT = 4
N_HIDDEN = 4
N_LAYERS = 2

#T_DATA = [input_, output_]
L_RATE = 0.5
E_BOUND = 0.000001

network = N(N_IN, N_OUT, N_HIDDEN, N_LAYERS, ALG_SET1)

network.set_bias(B)
network.load_weights(W)

#print(str(network.prop_values))
#print(str(network.weights))
network.propogate(I)

NPV = network.prop_values[network.total_layers - 1]

print(str(NPV))

""" THESE CAN AND SHOULD CAUSE ASSERTION ERRORS. """
#network.load_weights(BW)