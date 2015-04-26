from game import *
import numpy as np

class NeuronNetwork:
    """ Constructs a neuron network from an array of neuron arrays """
    def __init__(neuron_arrs_len, weights=None):
        if weights != None:
            self.weights = weights
        else:
            self.weights = []
            for i in range(len(neuron_arrs) - 1):
                len1 = neuron_arrs_len[i]
                len2 = neuron_arrs_len[i+1]
                self.weights.append(np.ones((len1, len2)))
    