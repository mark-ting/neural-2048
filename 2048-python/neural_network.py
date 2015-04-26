# -*- coding: utf-8 -*-
# neural_network.py
# Contains the code for a Neural Network object -- call by instantiation.

import numpy as np

class NeuralNetwork:
    def __init__(self, n_in, n_out, n_hidden, n_layers, weights, algorithm_set):
        self.n_in = n_in
        self.n_out = n_out
        self.n_hidden = n_hidden
        self.n_layers = n_layers
        self.algorithm_set = algorithm_set

        """ Initialize network weights """
        if weights is not None:
            self.weights = weights
        else:
            return 0
            # initialize weights as ones

    def propogate(self, n_in):
        """ Calculate values with nodes """
        # Step 1: Input -> Hidden
        # Step 2: Hidden -> Hidden (if n_hidden > 1)
        # Step 3: Hidden -> Output

    def load_weights(self, weight_list):
        """ Load weights from a list """

    def save_weights(self):
        """ Return weights as a list """

    def back_propogate(self, training, factor):
        """ Iterate over each layer--starting with H-O to update the output
            weights and then the input weights.
        """
        # update weight arrays #