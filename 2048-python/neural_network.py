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

        # Helper indices
        self.total_layers = n_layers + 2
        self.hidden_layers_exist = (n_layers != 0) & (n_hidden != 0)
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

        # Initialize weight values and previous changes for node interlinks
        #
        # Important indices:    w/c[0] = input-hidden
        #                       w/c[1 -> total_layers - 2] = h-h matrices
        #                       w/c[self.total_layers - 1] = h/i-o matrix
        self.weights = []
        self.changes = []  # previous set of changes

        if self.hidden_layers_exist:
            # Input-Hidden weights and changes
            self.weights.append(np.random.rand(self.n_hidden, self.n_in))
            self.changes.append(np.zeros((self.n_hidden, self.n_in)))

            # Hidden-Hidden weights and changes
            for i in range(self.n_layers - 1):  # handles multiple layers
                self.weights.append(np.random.rand(self.n_hidden,
                                                   self.n_hidden))
                self.changes.append(np.zeros((self.n_hidden, self.n_hidden)))

            # Hidden-Output weights and changes
            self.weights.append(np.random.rand(self.n_out, self.n_hidden))
            self.changes.append(np.zeros((self.n_out, self.n_hidden)))

        else:
            # Input-Output weights and changes
            self.weights.append(np.random.rand(self.n_out, self.n_in))
            self.changes.append(np.zeros((self.n_out, self.n_in)))

        # Initialize propogation and error value arrays
        self.prop_values = []
        self.error_values = []

        self.prop_values.append(np.zeros(self.n_in))
        self.error_values.append(np.ones(1))  # this should not be touched

        if self.hidden_layers_exist:
            # Hidden layer values and errors
            for i in range(self.n_layers):
                self.prop_values.append(np.zeros(self.n_hidden))
                self.error_values.append(np.zeros(self.n_hidden))

        # Output values and errors
        self.prop_values.append(np.zeros(self.n_out))
        self.error_values.append(np.zeros(self.n_out))

        # Sanity checks!
        assert len(self.prop_values) == self.total_layers, \
            "Propogation store is of the wrong size!"

        assert len(self.error_values) == self.total_layers, \
            "Error store is of the wrong size!"

        assert len(self.weights) == self.total_layers - 1, \
            "Weight store is of the wrong size!"

        assert len(self.changes) == self.total_layers - 1, \
            "Change store is of the wrong size!"

        assert len(self.weights) == len(self.changes), \
            "Weights and Change arrays are inconsistent!"

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
        last_weight = self.total_layers - 2

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
            signal = np.dot(self.weights[last_weight - 1][i, :],
                            self.prop_values[last_layer - 1])
            self.prop_values[last_layer][i] = self.clamp(signal)

        return(self.prop_values[last_layer])

    def back_propogate(self, template, learn_rate, momentum):
        """ Calculate error after a propogation run and adjust weights based
            on provided training data.

            Args:
                template:   expected output(s)
                learn_rate: how granular weight adjustments are
                momentum:   how much past rates of changes affect shifts

        """
        last_layer = self.total_layers - 1
        last_weight = self.total_layers - 2

        # Calculate output layer error
        print("Evaluating output error")
        for i in range(self.n_out):
            error = template[i] - (self.prop_values[last_layer])[i]
            prev_value = self.prop_values[last_layer][i]

            self.error_values[last_layer][i] = \
                error * self.grade(prev_value)

        # Calculate hidden layer error
        print("Evaluating hidden layer error")
        for i in range(self.n_layers):  # for each hidden layer...
            if i == 0:
                for j in range(self.n_hidden):
                    for k in range(self.n_out):
                        error = self.error_values[last_layer][k]
                        prev_value = self.prop_values[last_layer][k]

                        self.error_values[last_weight - i][j] = \
                            error * self.grade(prev_value)
            else:
                for l in range(self.n_hidden):
                    for m in range(self.n_hidden):
                        error = self.error_values[last_layer - i][l]
                        prev_value = self.prop_values[last_layer - i][l]

                        self.error_values[last_weight - i][m] = \
                            error * self.grade(prev_value)

        # Update output weights
        print("Adjusting output weights")
        for i in range(self.n_out):
            adjustment = self.error_values[last_layer][i] * \
                         self.prop_values[last_layer][i]
            new_weight = (learn_rate * adjustment) + \
                         (momentum * self.changes[last_weight][i])

            self.weights[last_weight][i] += new_weight
            self.changes[last_weight][i] = adjustment

        # Update hidden weights
        print("Adjusting hidden weights")
        for i in range(self.n_layers):  # for each hidden layer...
            for j in range(self.n_hidden):
                layer_index = last_layer - (i + 1)
                weight_index = last_weight - (i + 1)

                adjustment = self.error_values[layer_index][j] * \
                             self.prop_values[layer_index][j]

                new_weight = (learn_rate * adjustment) + \
                             (momentum * self.changes[weight_index][j])

                self.weights[weight_index][j] += new_weight
                self.changes[weight_index][j] = adjustment

        # Update input weights
        print("Adjusting input weights")
        for i in range(self.n_hidden):
            adjustment = self.error_values[1][i] * \
                         self.prop_values[1][i]

            new_weight = (learn_rate * adjustment) + \
                         (momentum * self.changes[0][i])

            self.weights[0][i] += new_weight
            self.changes[0][i] = adjustment

        total_error = 0.0
        for i in range(len(template)):
            total_error += \
                ((template[i] - self.prop_values[last_layer][i]) ** 2) / 2



    def load_weights(self, weights_in):
        """ Load weights from a provided file into the neural network """

        assert len(weights_in) == self.total_layers, \
            "Provided weight list is of the wrong size!"

        self.weights = weights_in

    def set_bias(self, bias):
        (self.prop_values[0])[self.n_in - 1] = bias

    def train(self, training_data, epoch, starting_weights=None):
        """ Train the neural network using provided training data.
            Return the weight matrix of the "trained" network.

            Args:
                training_data: tuples of (inputs, outputs) used
                epoch: iteration length
        """
        for e in range(epoch):
            for data_sets in len(training_data):
                inputs = training_data[data_sets][0]
                templates = training_data[data_sets][1]

            self.propogate(inputs)
            self.back_propogate(templates, 0.5, 0.3)

        return self.weights
