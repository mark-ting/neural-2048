# -*- coding: utf-8 -*-
# propogation_functions.py
# Contains triggering functions for neurons.

import numpy as np
import scipy as sp


def clamp_tanh(signal):
    return np.tanh(signal)


def clamp_expit(signal):
    return sp.expit(signal)


def expit_prime(output):
    return 1 - (output ** 2)


def tanh_prime(output):
    return 1 - (output ** 2)
