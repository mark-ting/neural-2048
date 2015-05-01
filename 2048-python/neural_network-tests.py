import numpy as np
from neural_network import NeuralNetwork as N
from propagation_functions import tanh, tanh_prime, expit, expit_prime, \
                                  linear, linear_prime

ALG_SET0 = (linear, linear_prime)
ALG_SET1 = (tanh, tanh_prime)
ALG_SET2 = (expit, expit_prime)

N_IN = 8
N_OUT = 4
N_HIDDEN = 4
N_LAYERS = 2

I = np.ones(N_IN)  # input set
B = 3

T_DATA = [0, 0, 0, 1]
ZERO = np.zeros(8)

BW = [[0,0], [0], [1, 2, 3, 2]]  # BAD WEIGHT MATRIX; USE TO BREAK THINGS.

L_RATE = 0.5
M_VAL = 0.3

network = N(N_IN, N_OUT, N_HIDDEN, N_LAYERS, ALG_SET1)

network.set_bias(B)

result = network.propogate(I)
network.back_propogate(T_DATA, L_RATE, M_VAL)

print(result)

""" THESE CAN AND SHOULD CAUSE ASSERTION ERRORS. """
# network.load_weights(BW)
