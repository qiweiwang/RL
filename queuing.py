import numpy as np
import sys

def thruput_reward(admission):
    return admission

def queue_len_reward(s_q):
    return -1*s_q

def q_est(theta, feature):
    if type(theta) == np.ndarray and type(feature) == np.ndarray:
        return theta.dot(feature.T)
    else
        print "type error!"
        return

def qlearn(feature, size, tr, qr, c):
    action = np.zeros()

if __name__ = "main":
