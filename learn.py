import sys
import numpy as np
import copy

from queue import Queue
import simulator

totalQueues = 2

class Agent:

    def __init__(self, queues, qTable, exploit_p, arr_p, snr):
        self.numberOfQueues = len(queues)
        self.currentQueues = queues
        self.currentState = ''
        #current state is always a string consists of current queue length separated by colomn.
        #example: '1,3'
        for i in self.currentQueues:
            self.currentState = self.currentState+str(i.currentLeng)+','
        self.currentState = self.currentState[:-1]
        self.qTable = qTable
        self.numberOfEpoch = 0
        self.exploit_p = exploit_p
        self.stepSimulator = simulator.MultiSimulator(arr_p, snr)
        self.reward = 0
        self.action = []

    # take one epoch action by:
    #   find a mixed/deterministic policy by glie
    #   run one step simulation and update action taken: action is always deterministic
    #   update queue lengthes and states accordingly
    def takeAction(self):
        [ad_policy, tx_policy] = self.glie()
        [self.reward, self.action] = self.stepSimulator.sim(self.currentQueues, ad_policy, tx_policy)
        self.numberOfEpoch  = self.numberOfEpoch + 1
        self.currentState = ''
        for i in self.currentQueues:
            self.currentState = self.currentState+str(i.currentLeng)

    # decide: explore or exploit
    def glie(self):
        if np.random.random()<self.exploit_p:
            [ad_policy,tx_policy] = self.findPolicy()
        else:
            [ad_policy,tx_policy] = self.explorePolicy()
        return [ad_policy, tx_policy]

    # find policy according q table
    def findPolicy(self):
        #for test purpose
        ad_policy = np.array([1, 0])
        tx_policy = np.array([0, 1])
        return [ad_policy, tx_policy]
        #for real q(s, a) table
        # ad_policy = np.zeros(self.numberOfQueues)
        # tx_policy = np.zeros(self.numberOfQueues)
        # maxAct = ''
        # maxValue = -100000000000
        # for act in qTable[self.currentState].keys():
        #     if qTable[self.currentState][act] > maxValue:
        #         maxValue = Table[self.currentState][act]
        #         maxAct = act
        # ad_policy[int(act[0])] = 1
        # tx_policy[int(act[1])] = 1
        # return [ad_policy, tx_policy]
    def explorePolicy(self):
        ad_policy = np.array([0, 1])
        tx_policy = np.array([1, 0])
        return [ad_policy, tx_policy]


class QTable():
    # q table: in this version of q table, only deterministic policy is considered
    #   label tier 1: state,deparsed, same format as agent.currentState
    #   label tier 2: 'a,b', a is queue number to enqueue, b is queue number ot dequeue, 'x' means doing nothing
    #   value: value of take action (label tier 2) at state (label tier 1)
    #   because only deterministic policy is considered, when a queue is full, the first char in tier 2 label has to be
    #   x. when a queue is 
    def __init__(self, queueLen):
        self.numberOfQueues = len(queueLen)
        self.table = {}
        for stateParsed in findAllStates(queueLen):
            state = stateDeParse(stateParsed)
            table[state] = {'x,x':0}
            for i in range(numberOfQueues):
                if stateParsed[i] != queueLen[i]:
                    table[state][str(i)+'x'] = 0
                    for j in range(numberOfQueues):
                        if (stateParsed[j] != 0):
                            table[state][str(i)+str(j)] = 0
                else:
                    for j in range(numberOfQueues):
                        if (stateParsed[j] != 0):
                            table[state]['x'+str(j)] = 0

    def setZero(self):
        for state in self.table.keys():
            for act in self.table[state].keys():
                self.table[state][act] = 0





def findAllStates(queueLenParsed):
    if len(queueLenParsed) == 1:
        result = []
        for i in range(queueLenParsed[0]+1):
            result.append([i])
        return result
    else:
        resultPrev = findAllStates(queueLenParsed[:-1])
        #print resultPrev
        result = []
        for statePrev in resultPrev:
        #    print statePrev
            for i in range(queueLenParsed[-1]+1):
                state = copy.copy(statePrev)
                state.append(i)
                result.append(state)
        return result


def stateParse(stateStr):
    stateStrSplit = stateStr.split(',')
    stateParsed = []
    for state in stateStrSplit:
        stateParsed.append(int(state))
    return stateParsed

def stateDeParse(stateParsed):
    stateStr = ''
    for state in stateParsed:
        stateStr = stateStr + str(state) + ','
    stateStr = stateStr[:-1]
    return stateStr


if __name__ == '__main__':
    #for i in range(totalQueues):

    #print stateParse('2,3,5,6')

    r = findAllStates(stateParse('5,6,10'))
    for i in r:
        rDeParse = stateDeParse(i)
        print rDeParse
    # print r
    # print len(r)

    # queue0 = Queue(3)
    # queue1 = Queue(4)
    # arr_p = [1, 1]
    # snr = [3.5, 12.0]
    # queues = [queue0, queue1]
    #
    # qTable = {}
    # agent = Agent(queues, qTable, 0.5, arr_p, snr)
    # print 'Agent created'
    # print 'number of queues is {}'.format(agent.numberOfQueues)
    #
    # while(1):
    #     print ''
    #     print 'New epoch, epoch number is {}'.format(agent.numberOfEpoch)
    #     print 'current state is ' + agent.currentState
    #     print 'instant reward is {}'.format(agent.reward)
    #     print 'exploit probability is {}'.format(agent.exploit_p)
    #     print 'take action...'
    #     agent.takeAction()
    #     print '*********************After action***********************'
    #     print 'number of queues is {}'.format(agent.numberOfQueues)
    #     print 'current state is ' + agent.currentState
    #     print 'instant reward is {}'.format(agent.reward)
    #     print 'exploit probability is {}'.format(agent.exploit_p)
    #     print 'actual action taken is'
    #     print agent.action
    #     if agent.numberOfEpoch > 10:
    #         break
