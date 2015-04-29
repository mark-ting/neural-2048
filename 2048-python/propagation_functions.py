# -*- coding: utf-8 -*-
# propogation_functions.py
# Contains triggering functions for neurons.

import numpy as np
import scipy as sp


def tanh(signal):
    return np.tanh(signal)


def expit(signal):
    return sp.special.expit(signal)


def expit_prime(output):
    return 1 - (output ** 2)


def tanh_prime(output):
    return 1 - (output ** 2)


def linear(signal):
    return signal

def linear_prime(output):
    return 1
