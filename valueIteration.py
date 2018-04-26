import numpy as np
from learnTx import *

import math
import copy

global weight
weight = [[39, 0.05], [39, 0.1]]
global snr
snr = [5.0,5.0]
# this policy iteration only works for 2 queues policy iteration

# Given state, next state and action, return transition probability (THE MODEL)
class valueIterator:

    def __init__(self, stateSpace, actionSpace, beta, arr_p):
        self.stateSpace = sorted(stateSpace)
        self.actionSpace = actionSpace
        self.vTable = dict((k, 200) for k in stateSpace)
        self.beta = beta
        self.arr_p = arr_p
        self.total0 = stateToList(self.stateSpace[-1])[0]
        self.total1 = stateToList(self.stateSpace[-1])[1]

    def transitionP(self, s0, s1, action):
        total0 = self.total0
        total1 = self.total1
        arr_p = self.arr_p
        #print action
        s0_queue = np.array(stateToList(s0))
        #print s0_queue
        s1_queue = np.array(stateToList(s1))
        #print s1_queue

        # print total0
        # print total1

        if np.any(s0_queue < np.array([0,0])) or  np.any(s0_queue > np.array([total0,total1])):
            return -1

        if np.any(s1_queue < np.array([0,0])) or  np.any(s1_queue > np.array([total0,total1])):
            return -2

        if abs(s0_queue[0]-s1_queue[0])>=2 or abs(s0_queue[1]-s1_queue[1])>=2:
            return 0

        if action == '001':

            diff = np.subtract(s0_queue, s1_queue)
            #print diff
            if s0_queue[0] == total0 and s0_queue[1] == total1:
                if np.all(diff == np.array([0,0])):
                    return 1
                else:
                    return 0
            elif s0_queue[0] == total0:
                #print k
                if np.all(diff == np.array([0,0])):
                    return 1-arr_p[1]
                elif np.all(diff == np.array([0,-1])):
                    return arr_p[1]
                else:
                    return 0
            elif s0_queue[1] == total1:
                if np.all(diff == np.array([0,0])):
                    return 1-arr_p[0]
                elif np.all(diff == np.array([-1,0])):
                    return arr_p[0]
                else:
                    return 0

            if np.any(diff > 0):
                return 0
            elif np.all(diff == np.array([-1,-1])):
                return arr_p[0]*arr_p[1]
            elif np.all(diff == np.array([-1,0])):
                return arr_p[0]*(1-arr_p[1])
            elif np.all(diff == np.array([0,-1])):
                return arr_p[1]*(1-arr_p[0])
            elif np.all(diff == np.array([0,0])):
                return (1-arr_p[1])*(1-arr_p[0])
            else:
                return -3

        if action == '010':
            diff = np.subtract(s0_queue, s1_queue)
            if s0_queue[1] == 0 and s0_queue[0] == total0:
                if diff[0] > 0:
                    return 0
                if np.all(diff == np.array([0,0])):
                    return 1-arr_p[1]
                if np.all(diff == np.array([0,-1])):
                    return arr_p[1]
            elif s0_queue[1] == 0:
                if diff[0] > 0:
                    return 0
                if np.all(diff == np.array([0,0])):
                    return (1-arr_p[0])*(1-arr_p[1])
                if np.all(diff == np.array([0,-1])):
                    return (1-arr_p[0])*arr_p[1]
                if np.all(diff == np.array([-1,0])):
                    return arr_p[0]*(1-arr_p[1])
                if np.all(diff == np.array([-1,-1])):
                    return arr_p[0]*arr_p[1]
            elif s0_queue[0] == total0:
                if diff[1] < 0 or diff[0] > 0:
                    return 0
                if np.all(diff == np.array([0,0])):
                    return arr_p[1]
                if np.all(diff == np.array([0,1])):
                    return 1-arr_p[1]
            else:
                if diff[1] < 0 or diff[0] > 0:
                    return 0
                if np.all(diff == np.array([0,1])):
                    return (1-arr_p[0])*(1-arr_p[1])
                if np.all(diff == np.array([0,0])):
                    return (1-arr_p[0])*arr_p[1]
                if np.all(diff == np.array([-1,1])):
                    return arr_p[0]*(1-arr_p[1])
                if np.all(diff == np.array([-1,0])):
                    return arr_p[0]*arr_p[1]
            return -4

        if action == '100':
            diff = np.subtract(s0_queue, s1_queue)
            if s0_queue[0] == 0 and s0_queue[1] == total1:
                if diff[1] > 0:
                    return 0
                if np.all(diff == np.array([0,0])):
                    return 1-arr_p[0]
                if np.all(diff == np.array([-1,0])):
                    return arr_p[0]
            elif s0_queue[0] == 0:
                if diff[1] > 0:
                    return 0
                if np.all(diff == np.array([0,0])):
                    return (1-arr_p[0])*(1-arr_p[1])
                if np.all(diff == np.array([0,-1])):
                    return (1-arr_p[0])*arr_p[1]
                if np.all(diff == np.array([-1,0])):
                    return arr_p[0]*(1-arr_p[1])
                if np.all(diff == np.array([-1,-1])):
                    return arr_p[0]*arr_p[1]
            elif s0_queue[1] == total1:
                if diff[0] < 0 or diff[1] > 0:
                    return 0
                if np.all(diff == np.array([0,0])):
                    return arr_p[0]
                if np.all(diff == np.array([1,0])):
                    return 1-arr_p[0]
            else:
                if diff[0] < 0 or diff[1] > 0:
                    return 0
                if np.all(diff == np.array([1,0])):
                    return (1-arr_p[0])*(1-arr_p[1])
                if np.all(diff == np.array([0,0])):
                    return (1-arr_p[1])*arr_p[0]
                if np.all(diff == np.array([1,-1])):
                    return arr_p[1]*(1-arr_p[0])
                if np.all(diff == np.array([0,-1])):
                    return arr_p[0]*arr_p[1]
            return -5

    def eReward(self,thisState, action):
        reward = 0
        for nextState in self.stateSpace:
            p = self.transitionP(thisState, nextState, action)
            # print nextState
            # print p
            if p > 0:
                reward = reward + p*self._fixReward(thisState, nextState, action)
        return reward

    def _fixReward(self, thisState, nextState, action):
        thisStateList = stateToList(thisState)
        nextStateList = stateToList(nextState)
        rwd_dly0 = -1*math.exp(nextStateList[0])*weight[0][1]
        rwd_dly1 = -1*math.exp(nextStateList[1])*weight[1][1]
        if (thisStateList[0]==0 and action == '100') or (thisStateList[1]==0 and action == '010'):
            rwd_cost = 0
        elif action == '001':
            rwd_cost = 0
        elif action == '100':
            rwd_cost = -1/snr[0]
        elif action == '010':
            rwd_cost = -1/snr[1]

        if action == "001":
            rwd_thu0 = (nextStateList[0]-thisStateList[0])*weight[0][0]
            rwd_thu1 = (nextStateList[1]-thisStateList[1])*weight[1][0]
            #print rwd_dly0+rwd_dly1+rwd_cost+rwd_thu0+rwd_thu1
            return rwd_dly0+rwd_dly1+rwd_cost+rwd_thu0+rwd_thu1

        if action == "100":
            if thisStateList[0] == 0:
                rwd_thu0 = (nextStateList[0]-thisStateList[0])*weight[0][0]
            else:
                rwd_thu0 = (nextStateList[0]-thisStateList[0]+1)*weight[0][0]
            rwd_thu1 = (nextStateList[1]-thisStateList[1])*weight[1][0]
            #print "one step reward is {}".format(rwd_dly0+rwd_dly1+rwd_cost+rwd_thu0+rwd_thu1)
            return rwd_dly0+rwd_dly1+rwd_cost+rwd_thu0+rwd_thu1

        if action == "010":
            rwd_thu0 = (nextStateList[0]-thisStateList[0])*weight[0][0]
            if thisStateList[1] == 0:
                rwd_thu1 = (nextStateList[1]-thisStateList[1])*weight[1][0]
            else:
                rwd_thu1 = (nextStateList[1]-thisStateList[1]+1)*weight[1][0]
            #print rwd_dly0+rwd_dly1+rwd_cost+rwd_thu0+rwd_thu1
            return rwd_dly0+rwd_dly1+rwd_cost+rwd_thu0+rwd_thu1

    def iteration(self, numberOfEpoch):
        self.vTableNext = copy.copy(self.vTable)
        self.actionTable = dict((k, '001') for k in stateSpace)
        for i in range(numberOfEpoch):
            print 'Epoch Number: {}'.format(i)
            for s in self.stateSpace:
                vNext = -10000000
                for a in self.actionSpace:
                    v = self.eReward(s,a)
                    for sNext in self.stateSpace:
                        v = v + self.beta*self.transitionP(s, sNext, a)*self.vTable[sNext]
                    if v > vNext:
                        vNext = v
                        self.actionTable[s] = a
                self.vTableNext[s] = vNext
            self.vTable = copy.copy(self.vTableNext)
            self._printTable(self.vTable)
            # self._printTable(self.actionTable)
            self._printPolicy()
            # raw_input('press any key to continue')

    def _printPolicy(self):
        print '   ',
        for i in range(self.total0+1):
            print '{:3s}'.format(str(i)),
        print ''
        for j in range(self.total1+1):
            print '{:3s}'.format(str(j)),
            for k in range(self.total0+1):
                state = str(k)+','+str(j)
                if self.actionTable[state] == '100':
                    print '{:3s}'.format('+'),
                else:
                    if self.actionTable[state] == '010':
                        print '{:3s}'.format('-'),
                    else:
                        print '{:3s}'.format('o'),
            print ''

    def _printTable(self, table):
        print '*********************************************'
        for key in sorted(table.keys()):
            print '{:5s}'.format(key),
            print table[key]
        print '*********************************************'









if __name__ == "__main__":
    stateSpaceList = findAllStates([6,6])
    stateSpace = []
    for stateList in stateSpaceList:
        stateSpace.append(listToState(stateList))

    vi = valueIterator(stateSpace, ['100', '010', '001'], 0.95, [0.45, 0.45])
    #print vi.eReward('0,1', '100')
    vi.iteration(150)
    fileName = 'policy.txt'
    fd = open(fileName, 'w')
    for key in sorted(vi.actionTable.keys()):
        fd.write(key),
        fd.write(' '),
        fd.write(vi.actionTable[key])
        fd.write('\n')
    fd.close()


    #print vi.transitionP('3,2','3,2','010')
    # print transitionP('2,11', '-2,-2', '100', [0.2, 0.4],10, 10)
