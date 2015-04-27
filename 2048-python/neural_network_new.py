# -*- coding: utf-8 -*-
# neural_network.py
# Contains the code for a Neural Network object -- call by instantiation.

import numpy as np
from propagation_functions import tanh, tanh_prime

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
            self.clamp = tanh
            self.grade = tanh_prime

        self.total_layers = n_layers + 2

        # Initialize interconnection weight values
        self.weights = []

        if self.hidden_layers_exist:

            # Input-Hidden matrix
            self.weights.append(np.random.rand(self.n_in - 1, self.n_hidden))

            # Hidden-Hidden matrices
            for i in range(self.n_layers):
                self.weights.append(np.random.rand(self.n_hidden,
                                                   self.n_hidden))

            # Hidden-Output matrix
            self.weights.append(np.random.rand(self.n_hidden, self.n_out))

        else:
            # Input-Output matrix
            self.weights.append(np.random.rand(self.n_in - 1, self.n_out))

        # Initialize propogation value arrays
        self.prop_values = []

        self.prop_values.append(np.zeros(self.n_in))  # input values

        if self.hidden_layers_exist:
            for i in range(self.n_layers):
                self.prop_values.append(np.zeros(self.n_hidden))

        self.prop_values.append(np.zeros(self.n_out))  # output values

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

        last_layer = self.total_layers - 1
        last_weight = last_layer - 1

        # Evaluate input layer (assigns input values to propogation array)
        print("Evaluating input layer")
        for i in range(self.n_in - 1):
            (self.prop_values[0])[i] = inputs[i]

        print(str(self.prop_values[0]))

        # Evaluate hidden layers
        print("Evaluating hidden layers")
        for i in range(self.n_layers):  # for each layer...
            for j in range(self.n_hidden):  # for each node
                # INNER PRODUCT OF WEIGHT ROW IN MATRIX AND PREVIOUS PROP_VAL
                signal = np.dot((self.weights[i])[j, :], self.prop_values[i + 1])
                print(str(signal))  # diagnostic output

        # Evaluate output layer
        print("Evaluating output layer")
        for i in range(self.n_out):
            signal = np.dot((self.weights[last_weight])[i, :],
                            self.prop_values[last_layer - 1])
            print(str(signal))
            #(self.prop_values[last_layer])[i] = self.clamp(signal)

    def load_weights(self, weights_in):
        """ Load weights from a provided file into the neural network """

        assert len(weights_in) == self.total_layers, \
            "Provided weight list is of the wrong size!"

        self.weights = weights_in

    def save_weights(self):
        """ Return weights as a list1 """
        return self.weights

    def back_propogate(self, training_data, learn_rate, error_bound):
        return 0
"""
        last_layer = self.total_layers - 1
        last_weight = self.total_layers - 2

        if self.hidden_layer_exists:

            # Update hidden-output weights
            for i in range(n_out):
                error = training_data[i] - self.prop_values[i]
                weight = self.grade((self.prop_values[last_layer])[i])

        else:
            # Update hidden output weights
        err = 0.0
        for i in range(len(training_data)):
            err = (training_data[i] - (self.prop_values[last_layer]) ** 2) / 2"""
""" Iterate over each layer--starting with H-O to update the output
    weights and then the input weights.
"""
# update weight arrays #