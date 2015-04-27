# -*- coding: utf-8 -*-
# neural_network.py
# Contains the code for a Neural Network object -- call by instantiation.

import numpy as np
from propagation_functions import clamp_tanh as ctanh, \
                                 tanh_prime as tanhp, \
                                 clamp_expit as cexpit, \
                                 expit_prime as expitp

# from algorithms import clamp, d_clamp


class NeuralNetwork:
    def __init__(self, n_in, n_out, n_hidden, n_layers, algorithm_set):

        """ Initialize number of nodes and layers """
        self.n_in = n_in + 1    # add 1 to account for bias node
        self.n_out = n_out
        self.n_hidden = n_hidden
        self.n_layers = n_layers
        self.algorithm_set = algorithm_set

        self.total_layers = 2 + n_layers
        self.weights = []

        """ Initialize interconnection weight values """
        if n_layers != 0:
            # Number of connections between input and hidden layers
            ih_inter = (n_in) * (n_hidden)

            # Number of connections between interior hidden layers
            hh_inter = ((n_hidden + 1) * (n_hidden))  # interlayer connections
            hh_total = (hh_inter) ** (n_layers - 1)   # total over all layers

            # Number of connections between hidden and output layers
            ho_inter = (n_hidden) * (n_out)

            # Add the arrays of weight values (1.0 right now) to the list
            self.weights.append(np.ones(ih_inter))

            for i in range(n_layers - 1):
                self.weights.append(np.ones(hh_inter))

            self.weights.append(np.ones(ho_inter))

        else:
            io_inter = (n_in) * (n_out)
            self.weights.append(np.ones(io_inter))

        """ Initialize node propogation values """
        self.prop_values = []

        self.prop_values.append(np.ones(n_in))

        for i in range(self.n_layers):
            self.prop_values.append(np.ones(n_hidden))

        self.prop_values.append(np.ones(n_out))

        assert len(self.prop_values) == self.total_layers, \
            "Propogation array size mismatch!"

    # TODO: MAKE THIS WORK.
    def propogate(self, inputs):
        """Calculate outputs using provided inputs.
        Propagates through all defined nodes using currently assigned weight
        values.

        IMPORTANT: THIS DOES NOT UPDATE THE WEIGHT VALUES!
        (See back_propogate for updating weight values.)

        NOTE: inputs should be a list built from parsing the game data for
        specified heuristics!

        In this case: R0-R3 and C0-C3 de/ascending? (Monotonicity)
        """

        assert len(inputs) == self.n_in - 1, \
            "Input incompatible with number of input nodes!"  # should be 8

        # TODO: MAKE EVALUATIONS ACTUALLY EVALUATE INSTEAD OF PRINTING!

        # Evaluate input layer (assigns input values to propogation array)
        print("Evaluating input layer")
        for i in range(self.n_in - 1):
            (self.prop_values[0])[i] = ctanh(inputs[i])
            print((self.prop_values[0])[i])   # TEST STATEMENT--REMOVE!

        # TODO: Evaluate hidden layers

        if self.n_layers != 0:
            # Step 2: Hidden -> Hidden (if n_hidden > 1)
            print("Evaluating hidden layers")
            for i in range(self.n_layers):

                for j in range(self.n_hidden):

                    signal = 0.0  # transmission

                    print((self.prop_values[i])[j])   # TEST STATEMENT--REMOVE!

                    if i == 0:
                        # first hidden layer takes input layer as previous
                        previous_layer_size = self.n_in - 1
                    else:
                        # subsequent layers take hidden layers as previous
                        previous_layer_size = self.n_hidden

                    for k in range(previous_layer_size):
                        signal += (self.weights[i + 1])[k] * \
                                  (self.prop_values[0])[k]

                    # TODO: DOUBLE CHECK THE MATH ON THIS
                    (self.prop_values[i + 1])[j] = ctanh(signal)

            # TODO: Evaluate output layer
            print("Evaluating output layer")
            for i in range(self.n_out):
                signal = 0.0
                for j in range(self.n_hidden):
                    signal += (self.prop_values[i])[j]
                    # TODO: ADD IN PROCESSING AND CLAMPING
                    print((self.prop_values[self.total_layers - 1])[i])
                    # TEST STATEMENT--REMOVE!
                (self.prop_values[i + 1])[j] = ctanh(signal)

        else:
            print("Evaluating output layer")
            for i in range(self.n_out):

                signal == 0.0

                for j in range(self.n_in):
                    signal += (self.weights[self.total_layers - 1])[j]


    def load_weights(self, weights_in):
        """ Load weights from a provided file into the neural network """

        assert len(weights_in) == self.total_layers, \
            "Provided weight list is of the wrong size!"

        self.weights = weights_in

    def save_weights(self):
        """ Return weights as a list """
        return self.weights

    def back_propogate(self, training_data, learn_rate, error_bound):
        """ Iterate over each layer--starting with H-O to update the output
            weights and then the input weights.
        """
        # update weight arrays #
