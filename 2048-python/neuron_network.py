from game import *
import numpy as np

class NeuronNetwork:
    """ Constructs a neuron network from an array of neuron arrays """
    def __init__(neuron_arrs, weights=None):
        if weights != None:
            self.weights = weights
        else:
            self.weights = []
            for i in range(len(neuron_arrs) - 1):
                len1 = len(neuron_arrs[i])
                len2 = len(neuron_arrs[i+1])
                self.weights.append(np.ones((len1, len2)))
    