from learnTx import *

import sys
import numpy as np
import copy
import operator
import math
import random

from queue import Queue
import simulator

from tabulate import tabulate

class Evaluator:
    def __init__(self, policy, queues, arr_p, snr, weight, beta):
        self.policy = policy
        self.queues = queues
        self.currentState = ''
        #current state is always a string consists of current queue length separated by colomn.
        #example: '1,3'
        for i in self.queues:
            self.currentState = self.currentState+str(i.currentLeng)+','
        self.currentState = self.currentState[:-1]
        self.totalReward = 0
        self.stepSimulator = simulator.MultiSimulator(arr_p, snr, weight)
        self.beta = beta

    def evaluate(self, steps):
        for step in range(steps):
            action = self.policy[self.currentState]
            [self.reward, self.actionTaken] = self.stepSimulator.simTx(self.queues, actionToArray(action))
            self.actionTaken = action
            self.totalReward = self.totalReward + self.reward
            self.currentState = ''
            for i in self.queues:
                self.currentState = self.currentState+str(i.currentLeng) + ','
            self.currentState = self.currentState[:-1]
            # print "step: {}".format(step)
            # print "action taken is: {}".format(self.actionTaken)
            # print "instant reward is: {}".format(self.reward)
            # print "current state is: {}".format(self.currentState)
            # print "total reward is: {}".format(self.totalReward)
            # print "***************************************************************************"
            if np.random.random()< (1-self.beta):
                break;

if __name__ == "__main__":
    arg = sys.argv[1:]
    # queue0 = Queue(6,2)
    # queue1 = Queue(6,5)
    # queue2 = Queue(6,3)
    # queue3 = Queue(6,3)
    # queues = [queue0, queue1, queue2, queue3]
    policy = {}
    fd = open('policy_theta' + str(arg[0])+'.txt', 'r')
    while(1):
        try:
            line = fd.readline()
            [key, value] = line.split(' ')
            policy[key] = value[:-1]
        except:
            break

    print len(policy)

    rewardAverage = 0
    for simNumber in range(15000):
        if simNumber%1000 == 0:
            print(simNumber)
        queue0 = Queue(6,2)
        queue1 = Queue(6,5)
        queue2 = Queue(9,3)
        queue3 = Queue(8,3)
        queues = [queue0, queue1, queue2, queue3]
        # ev = Evaluator(policy, queues, [0.45, 0.45], [5.0, 5.0], [[39, 0.05], [39, 0.1]] , 0.95)
        ev = Evaluator(policy, queues, [0.1, 0.2, 0.3, 0.25], [5.0, 5.0, 10.0, 10.0], [[39, 0.05], [20, 0.1], [39, 0.15], [10, 0.25]], 0.95)
        # ev = Evaluator(policy, queues, [0.2, 0.2, 0.2, 0.2], [7.0, 5.0, 5.0, 7.0], [[39, 0.05], [39, 0.15], [39, 0.08], [39, 0.05]], 0.95)
        ev.evaluate(10000)
        rewardAverage = rewardAverage + ev.totalReward
    rewardAverage = rewardAverage/15000
    print rewardAverage
