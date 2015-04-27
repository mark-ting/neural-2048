# -*- coding: utf-8 -*-
# neural_network.py
# Contains the code for a Neural Network object -- call by instantiation.

import numpy as np
from propagation_functions import clamp_tanh as ctanh, \
                                 tanh_prime as tanhp, \
                                 clamp_expit as cexpit, \
                                 expit_prime as expitp


class NeuralNetwork:
    def __init__(self, n_in, n_out, n_hidden, n_layers, function_set=None):

        """ Initialize number of nodes and layers """
        self.n_in = n_in + 1  # add 1 to account for bias node
        self.n_out = n_out
        self.n_hidden = n_hidden
        self.n_layers = n_layers

        # Check if hidden layers exist
        self.hidden_layers_exist = (n_layers != 0)

        # Set clamping and gradient functions
        if function_set is not None:

            assert len(function_set) == 2, \
                "Provide a set of TWO functions."

            # Load functions from provided set
            self.clamp = function_set[0]
            self.grade = function_set[1]

        else:
            # Default to hyperbolic tangent and its derivative
            self.clamp = ctanh
            self.grade = tanhp

        self.total_layers = n_layers + 2
        self.weights = []

        """ Initialize interconnection weight values """
        if self.hidden_layers_exist:

            # Number of connections between input and hidden layers
            ih_inter = (n_in) * (n_hidden)

            # Number of connections between interior hidden layers
            hh_inter = ((n_hidden + 1) * (n_hidden))

            # Number of connections between hidden and output layers
            ho_inter = (n_hidden) * (n_out)

            # Add the arrays of weight values (1.0 right now) to the list
            self.weights.append(np.ones(ih_inter))

            for i in range(n_layers - 1):
                self.weights.append(np.ones(hh_inter))

            self.weights.append(np.ones(ho_inter))

        else:

            # Number of connections between input and output layers
            io_inter = (n_in) * (n_out)
            self.weights.append(np.ones(io_inter))

        """ Initialize node propogation values """
        self.prop_values = []

        self.prop_values.append(np.ones(n_in))  # add input nodes

        for i in range(self.n_layers):
            self.prop_values.append(np.ones(n_hidden))  # add hidden nodes

        self.prop_values.append(np.ones(n_out))  # add output nodes

        assert len(self.prop_values) == self.total_layers, \
            "Propogation array size mismatch!"

    # TODO: DOUBLE CHECK THIS WORKS
    def propogate(self, inputs):
        """Calculate outputs using provided inputs.
        Propagates through all defined nodes using currently assigned weight
        values.

        IMPORTANT: THIS DOES NOT UPDATE THE WEIGHT VALUES!
        (See back_propogate for updating weight values.)

        NOTE: inputs should be a list built from parsing the game data for
        specified heuristics!
        """
        assert len(inputs) == self.n_in - 1, \
            "Input incompatible with number of input nodes!"

        # Evaluate input layer (assigns input values to propogation array)
        print("Evaluating input layer")
        for i in range(self.n_in - 1):
            (self.prop_values[0])[i] = inputs[i]
            print((self.prop_values[0])[i])  # TEST PRINT

        # Since the last layer is zero-indexed by -1, and there are n - 1
        # weight arrays for n layers, last_weight index should be n - 2
        last_layer = self.total_layers - 1
        last_weight = self.total_layers - 2

        if self.hidden_layers_exist:
            # Step 2: Hidden -> Hidden (if n_hidden > 1)
            print("Evaluating hidden layers")
            for i in range(self.n_layers):
                for j in range(self.n_hidden):
                    signal = 0.0  # transmission

                    # Check to see if evaluating first hidden layer
                    if i == 0:
                        # First hidden layer takes input layer as previous
                        layer_before_hidden = self.n_in - 1

                    else:
                        # Subsequent layers take hidden layers as previous
                        layer_before_hidden = self.n_hidden

                    for k in range(layer_before_hidden):
                        signal += (self.weights[i])[k] * \
                                  (self.prop_values[0])[k]

                    # Hidden layers start at index 1, so + 1
                    (self.prop_values[i + 1])[j] = self.clamp(signal)
                    print((self.prop_values[i + 1])[j])  # TEST PRINT

        # Evaluate output layer
        print("Evaluating output layer")
        for i in range(self.n_out):
            signal = 0.0

            if self.hidden_layers_exist:
                layer_before_output = self.n_hidden
            else:
                layer_before_output = self.n_in - 1

            for j in range(layer_before_output):
                signal += (self.weights[last_weight])[j] * \
                          (self.prop_values[i])[j]

            (self.prop_values[last_layer])[i] = self.clamp(signal)  # clamp!
            print((self.prop_values[last_layer])[i])  # TEST PRINT

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
