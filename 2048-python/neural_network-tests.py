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

in_size = 4

I = np.ones(in_size)  # input set
B = 3

T_DATA = [0, 0, 0, 1]

ZERO = np.zeros(8)

BW = [[0,0], [0], [1, 2, 3, 2]]  # BAD WEIGHT MATRIX; USE TO BREAK THINGS.

N_IN = in_size
N_OUT = 2
N_HIDDEN = 3
N_LAYERS = 2

#T_DATA = [input_, output_]
L_RATE = 0.5
E_BOUND = 0.000001
M_VAL = 0.3

network = N(N_IN, N_OUT, N_HIDDEN, N_LAYERS, ALG_SET1)

network.set_bias(B)

network.propogate(I)
network.back_propogate(T_DATA, L_RATE, M_VAL)

""" THESE CAN AND SHOULD CAUSE ASSERTION ERRORS. """
#network.load_weights(BW)