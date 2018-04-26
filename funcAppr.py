import numpy as np
from utility import *
import sys
import numpy as np
import copy
import operator
import math
import random

from queue import Queue
from agents import Agent_fa
import simulator

class qFunc():

    def __init__(self, beta, learningRate, stateSpace, actionSpace, useRealQ = False):
        self.beta = beta
        self.learningRate = learningRate
        self.featureLen = len(stateSpace[0]) * len(actionSpace) + 1
        self.theta = np.random.rand(self.featureLen, 1)
        self.stateSpace = stateSpace #all state in list format
        self.actionSpace = actionSpace #all action in string format
        self.useRealQ = useRealQ
        if useRealQ:
            self.qTable = {}
            fd = open('qTable.txt', 'r')
            while(1):
                try:
                    line = fd.readline()
                    line = line[:-1]
                    values = line.split(" ")
                    # print values
                    self.qTable[values[0]] = {}
                    for index, a in enumerate(sorted(actionSpace, reverse = True)) :
                        self.qTable[values[0]][a] = float(values[index+1])
                except:
                    break
            fd.close()
            # print self.qTable


    def printQTable(self):
        if not self.useRealQ:
            print "no q table to print"
            return
        for state in sorted(self.qTable.keys()):
            print state.rjust(6),
            for action in sorted(self.qTable[state].keys(), reverse = True):
                print '{0:5.8f}'.format(self.qTable[state][action]),
            print ""
        return


    def output(self, feature):
        # input: a np_array with size (n,1)
        return np.dot(self.theta.T, feature)

    def updateTheta(self, reward, thisState, nextState, action, alpha):
        if self.useRealQ:
            estimateQ = self.qTable[listToState(thisState)][action]
        else:
            nextAction =  self.findMaxAction(nextState)
            estimateQ = reward + self.beta * self.output(self._toFeature(nextState, nextAction))
        self.theta = self.theta + self.learningRate*1000.0/(1000.0+alpha) * (estimateQ - self.output(self._toFeature(thisState, action)))*self._toFeature(thisState, action)
        return
    # def dtheta(self, state, action):
    #     return
    def _toFeature(self,stateList, action):
            # input state in string format, action in string format
            # output a feature vector that ith element is f(i)(s,a)
        feature = np.zeros((self.featureLen, 1))
        feature[0] = 1
        fFraction = np.array(stateList).reshape(len(stateList),1)
        for index, thisAction in enumerate(self.actionSpace):
            if thisAction == action:
                for i,s in enumerate(stateList):
                    feature[1+index*len(stateList)+i] = s
        return feature.reshape((self.featureLen, 1))
    def findMaxAction(self, stateList):
        q = -1*float('inf')
        maxAction = self.actionSpace[0]
        for action in self.actionSpace:
            if self.output(self._toFeature(stateList, action)) > q:
                maxAction = action
                q = self.output(self._toFeature(stateList, action))
        return maxAction
    def randomAction(self):
        i = int(math.floor(np.random.random()*len(self.actionSpace)))
        return actionToArray(actionSpace[i])

    def makePolicy(self, n = '0'):
        fd =  open("policy_theta"+n+".txt", "w")
        for s in self.stateSpace:
            for index, q in enumerate(s):
                if index == len(s)-1:
                    fd.write(str(q) + ' '),
                else:
                    fd.write(str(q) + ','),
            fd.write(self.findMaxAction(s)),
            fd.write("\n")

    def generateQTable(self):
        if not self.useRealQ:
            print 'need real q'
            return
        self.currentQTable = {}
        diff = 0
        for s in self.stateSpace:
            sList = listToState(s)
            self.currentQTable[sList] = {}
            for a in self.actionSpace:
                self.currentQTable[sList][a] = float(self.output(self._toFeature(s,a)))
                diff += abs(self.currentQTable[sList][a]-self.qTable[sList][a])
        return diff








def printPolicy(qFunc, qLen0, qLen1):
    if len(qFunc.actionSpace) > 3:
        print "too many states, cannot print"
        return
    print '   ',
    for i in range(qLen0+1):
        print '{:3s}'.format(str(i)),
    print ''
    for j in range(qLen1+1):
        print '{:3s}'.format(str(j)),
        for k in range(qLen0+1):
            state = [k,j]
            if qFunc.findMaxAction(state) == '100':
                print '{:3s}'.format('+'),
            else:
                if qFunc.findMaxAction(state) == '010':
                    print '{:3s}'.format('-'),
                else:
                    print '{:3s}'.format('o'),
        print ''




theta_history = []


# if __name__ == "__main__":
#             queue0 = Queue(6,2)
#             queue1 = Queue(6,5)
#             queue2 = Queue(9,3)
#             queue3 = Queue(8,3)
#             queues = [queue0, queue1, queue2, queue3]
#             # queues = [queue0, queue1]
#             stateSpace = findAllStates([x.totalLeng for x in queues])
#             actionSpace = findAllActions(len(queues))
#             qF = qFunc(0.95, 0.001, stateSpace, actionSpace, True)
#             qF.theta = np.array([1158.96, -28.41, -50.75, -211.36, -193.62, -28.41, -50.74, -206.98, -190.96, -31.36, -51.05, -140.97, -199.17, -31.15, -50.85, -213.98, -117.27, -28.41, -50.74, -218.24, -197.26])
#             print qF.generateQTable()
#             qF.makePolicy('SuperLong')
if __name__ == "__main__":
    if __name__ == "__main__":
        queue0 = Queue(6,2)
        queue1 = Queue(6,5)
        queue2 = Queue(9,3)
        queue3 = Queue(8,3)
        queues = [queue0, queue1, queue2, queue3]
        # queues = [queue0, queue1]
        stateSpace = findAllStates([x.totalLeng for x in queues])
        actionSpace = findAllActions(len(queues))
        qF = qFunc(0.95, 0.0005, stateSpace, actionSpace, True)
        print "discount value is {}".format(qF.beta)
        print "learning rate is {}".format(qF.learningRate)
        print "size of state space is {}".format(len(qF.stateSpace))
        print "action space is {}".format(qF.actionSpace)
        print "initial theta is {}".format(qF.theta)
        qF.printQTable()
        raw_input("Press Enter to continue...")

        diffHistory = []
        for e in range(800000):
            for queue in queues:
                queue.currentLeng = random.randrange(queue.totalLeng+1)
                # print "length is {}".format(queue.currentLeng)
            # agent = Agent_fa(queues, qF, 0.5, [0.2, 0.2, 0.2, 0.2], [7.0, 5.0, 5.0, 7.0], [[39, 0.05], [39, 0.15], [39, 0.08], [39, 0.05]])
            # agent = Agent_fa(queues, qF, 0.5, [0.45, 0.45], [5.0, 5.0], [[39, 0.05], [39, 0.1]])
            agent = Agent_fa(queues, qF, 0.5, [0.1, 0.2, 0.3, 0.25], [5.0, 5.0, 10.0, 10.0], [[39, 0.05], [20, 0.1], [39, 0.15], [10, 0.25]])
            if e% 100 == 0:
                print e
                print qF.theta
                diffHistory.append(qF.generateQTable())
                # qF.makePolicy(str(e))
            theta_history.append(qF.theta)
            for i in range(50):
                thisState =  agent.currentState
                # print "this state is {}".format(thisState)
                agent.takeAction()
                nextState =  agent.currentState
                # print "next state is {}".format(nextState)
                # print "action taken is {}".format(agent.actionTaken)
                # print "reward is {}".format(agent.reward)
                qF.updateTheta(agent.reward, thisState, nextState, arrayToAction(agent.actionTaken),e)
            # raw_input("Press Enter to continue...")

        printPolicy(qF, queue0.totalLeng, queue1.totalLeng)
        qF.makePolicy()

        fd = open("results and figures/theta_history.txt", 'w')
        i = 0
        for theta in theta_history:
            for n in theta:
                fd.write(str(float(n)))
                fd.write('\n')
        fd.close()

        fd = open("diffHistory.txt", 'w')
        for d in diffHistory:
                fd.write(str(float(d)))
                fd.write('\n')
        fd.close()
