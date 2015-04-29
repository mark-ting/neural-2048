# -*- coding: utf-8 -*-
# neural_network.py
# Contains the code for a Neural Network object -- call by instantiation.

import numpy as np
from propagation_functions import tanh, tanh_prime


class NeuralNetwork:
    def __init__(self, n_in, n_out, n_hidden, n_layers, function_set=None):

        # Initialize number of nodes and layers
        self.n_in = n_in + 1  # add 1 to account for bias node
        self.n_out = n_out
        self.n_hidden = n_hidden
        self.n_layers = n_layers

        self.total_layers = n_layers + 2            # helps indexing later
        self.hidden_layers_exist = (n_layers != 0)  # saves work later
        self.test = 0

        # Set clamping and gradient functions
        if function_set is not None:

            assert len(function_set) == 2, \
                "Provide a function set: (clamping_function, derivative_f)"

            # Load functions from provided set
            self.clamp = function_set[0]
            self.grade = function_set[1]

        else:
            # Default to hyperbolic tangent and its derivative
            self.clamp = tanh
            self.grade = tanh_prime

        # Initialize weight values for node interconnections
        self.weights = []

        if self.hidden_layers_exist:
            # Input-Hidden weights
            self.weights.append(np.random.rand(self.n_hidden, self.n_in))

            # Hidden-Hidden weights
            for i in range(self.n_layers):  # handles multiple layers
                self.weights.append(np.random.rand(self.n_hidden,
                                                   self.n_hidden))

            # Hidden-Output weights
            self.weights.append(np.random.rand(self.n_out, self.n_hidden))

        else:
            # Input-Output matrix
            self.weights.append(np.random.rand(self.n_out, self.n_in))

        # Initialize propogation and error value arrays
        self.prop_values = []
        self.error_values = []

        self.prop_values.append(np.zeros(self.n_in))  # no need for error (in!)

        if self.hidden_layers_exist:
            # Hidden layer values and errors
            for i in range(self.n_layers):
                self.prop_values.append(np.zeros(self.n_hidden))
                self.error_values.append(np.zeros(self.n_hidden))

        # Output values and errors
        self.prop_values.append(np.zeros(self.n_out))
        self.error_values.append(np.zeros(self.n_out))

        self.error_values.reverse  # sets output first (for error evaluation)

        # Sanity checks!
        assert len(self.prop_values) == self.total_layers, \
            "Propogation array is of the wrong size!"

        assert len(self.error_values) == self.total_layers - 1, \
            "Error array is of the wrong size!"

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
            self.prop_values[0][i] = inputs[i]

        # Evaluate hidden layers
        print("Evaluating hidden layer(s)")
        for i in range(self.n_layers):  # for each hidden layer...
            for j in range(self.n_hidden):  # for each node...
                signal = np.dot(self.weights[i][j, :],
                                self.prop_values[i])
                self.prop_values[i + 1][j] = self.clamp(signal)

        # Evaluate output layer
        print("Evaluating output layer")
        for i in range(self.n_out):
            signal = np.dot(self.weights[last_weight][i, :],
                            self.prop_values[last_layer - 1])
            self.prop_values[last_layer][i] = self.clamp(signal)

        return(self.prop_values[last_layer])

    def back_propogate(self, training, learn_rate):
        """ Calculate error after a propogation run and adjust weights based
            on provided training data.

            Args:
                training - set of expected outputs

        """
        last_layer = self.total_layers - 1
        h_start = self.total_layers - 2  # start hidden layers reverse index

        # Calculate output layer error
        print("Evaluating output error")
        for i in range(self.n_out):
            error = training[i] - (self.prop_values[last_layer])[i]
            self.error_values[0][i] = \
                error * self.grade((self.prop_values[last_layer])[i])

        # Calculate hidden layer error
        print("Evaluating hidden layer error")
        for i in range(self.n_layers):  # for each hidden layer...
            for j in range(self.n_hidden):
                error = np.dot(self.error_values[0], self.weights[i + 1][j, :])
                self.error_values[i + 1][j] = \
                    error * self.grade(self.prop_values[h_start - i][j])

        # Update output weights
        # Update hidden weights
        # Update input weights
        return self.error_values

    def load_weights(self, weights_in):
        """ Load weights from a provided file into the neural network """

        assert len(weights_in) == self.total_layers, \
            "Provided weight list is of the wrong size!"

        self.weights = weights_in

    def save_weights(self):
        """ Return weights as a list """
        return self.weights

    def set_bias(self, bias):
        (self.prop_values[0])[self.n_in - 1] = bias
