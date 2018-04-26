
import simulator
import numpy as np
import math
from utility import *

class Agent:

    def __init__(self, queues, qTable, exploit_p, arr_p, snr, weight):
        self.numberOfQueues = len(queues)
        self.currentQueues = queues
        self.currentState = ''
        #current state is always a string consists of current queue length separated by colomn.
        #example: '1,3'
        for i in self.currentQueues:
            self.currentState = self.currentState+str(i.currentLeng)+','
        self.currentState = self.currentState[:-1]
        self.qTable = qTable
        self.numberOfEpoch = 1
        self.exploit_p = exploit_p
        self.stepSimulator = simulator.MultiSimulator(arr_p, snr, weight)
        self.reward = 0
        self.actionTaken = []

    # take one epoch action by:
    #   find a mixed/deterministic policy by glie
    #   run one step simulation and update action taken: action is always deterministic
    #   update queue lengthes and states accordingly
    def takeAction(self):
        tx_action = self.glie()
        #print "action choosen is {}".format(tx_action)
        [self.reward, self.actionTaken] = self.stepSimulator.simTx(self.currentQueues, tx_action)
        self.actionTaken = tx_action
        self.numberOfEpoch  = self.numberOfEpoch + 1
        self.currentState = ''
        for i in self.currentQueues:
            self.currentState = self.currentState+str(i.currentLeng) + ','
        self.currentState = self.currentState[:-1]

    #def updataQTable(self):


    # decide: explore or exploit
    def glie(self):
        if np.random.random()<self.exploit_p:
            tx_action = self.findActionArray(True)
        else:
            tx_action = self.exploreActionArray()
        return tx_action

    # find policy according q table
    def findActionArray(self, useQ):
        if useQ:
            return actionToArray(self.qTable.findAction(self.currentState))
        else:
            return np.array([0,1,0])


    def exploreActionArray(self):
        i = int(math.floor(np.random.random()*len(findAllActions(self.numberOfQueues))))
        #print i
        tx_action = actionToArray(self.qTable.table[self.currentState].keys()[i])
        return  tx_action

class Agent_fa():

    def __init__(self, queues, qFunc, exploit_p, arr_p, snr, weight):
        self.numberOfQueues = len(queues)
        self.currentQueues = queues
        self.currentState = []
        #current state is always a string consists of current queue length separated by colomn.
        #example: '1,3'
        for i in self.currentQueues:
            self.currentState.append(i.currentLeng)
        self.qFunc = qFunc
        self.numberOfEpoch = 1
        self.exploit_p = exploit_p
        self.stepSimulator = simulator.MultiSimulator(arr_p, snr, weight)
        self.reward = 0
        self.actionTaken = []

    def takeAction(self):
        tx_action = self.glie()
        #print "action choosen is {}".format(tx_action)
        [self.reward, self.actionTaken] = self.stepSimulator.simTx(self.currentQueues, tx_action)
        self.actionTaken = tx_action
        self.numberOfEpoch  = self.numberOfEpoch + 1
        self.currentState = []
        for i in self.currentQueues:
            self.currentState.append(i.currentLeng)

    def glie(self):
        if np.random.random()<self.exploit_p:
            tx_action = self.findActionArray(True)
        else:
            tx_action = self.exploreActionArray()
        return tx_action

    def findActionArray(self, useQ):
        if useQ:
            return actionToArray(self.qFunc.findMaxAction(self.currentState))
        else:
            return np.array([0,1,0])

    def exploreActionArray(self):
        # print self.qFunc.randomAction()
        return self.qFunc.randomAction()
        # i = int(math.floor(np.random.random()*3))
        # #print i
        # tx_action = actionToArray(self.qTable.table[self.currentState].keys()[i])
        # return  tx_action
