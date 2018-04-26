import sys
import numpy as np
import copy
import operator
import math
import random

from queue import Queue
import simulator

from tabulate import tabulate
from utility import *
from agents import Agent

global qRecord
qRecord = []
q23 = []


class QTable():
    # q table: in this version of q table, only deterministic action is considered

    def __init__(self, queueLen):
        self.queueLen = queueLen
        self.numberOfQueues = len(queueLen)
        self.table = {}
        self.actionList = findAllActions(self.numberOfQueues)
        self.stateLists = findAllStates(queueLen)

        for stateList in self.stateLists:
            state = listToState(stateList)
            self.table[state] = {}
            for action in self.actionList:
                self.table[state][action] = [250.0, 1]

    def setZero(self):
        for state in self.table.keys():
            for act in self.table[state].keys():
                self.table[state][act] = [0.00, 1]

    def doSomethingToTable(self):
        for stateList in self.stateLists:
            state = listToState(stateList)
            self.table[state]['100'] = 0.76

    def updateTable(self, state, nextState, action, insReward, epoch):
        beta = 0.95
        nextValue = self.table[nextState][self.findAction(nextState)][0]
        discountValue = beta*nextValue
        if state == '2,5,3,3' and arrayToAction(action) == '01000':
            # qRecord.append([self.table[state]['010'][0], insReward + discountValue, nextState, nextValue])
            qRecord.append(self.table[state]['01000'][0])
        #print "old value is {}".format(self.table[state][arrayToAction(action)])
        self.table[state][arrayToAction(action)][0] = self.table[state][arrayToAction(action)][0] + 10.0/(9+self.table[state][arrayToAction(action)][1])*(insReward + discountValue - self.table[state][arrayToAction(action)][0])
        self.table[state][arrayToAction(action)][1] = self.table[state][arrayToAction(action)][1] + 1
        # if state == '2,3' and arrayToAction(action) == '010':
        #     qRecord.append([self.table[state]['010'][0], insReward + discountValue])

        #print "new value is {}".format(self.table[state][arrayToAction(action)])

    def findAction(self,state):
        return max(self.table[state].iteritems(), key=operator.itemgetter(1))[0]

    def printTable(self):
        for state in sorted(self.table.keys()):
            print state.rjust(6),
            for action in self.table[state].keys():
                print '{0:5.8f}'.format(self.table[state][action][0]),
                print '{0:7d}'.format(self.table[state][action][1]),
            print self.findAction(state).rjust(5),
            print ""
        # for action in self.table[state].keys():
        #     print action,
        # print "

    def printTableToFile(self):
        fd = open('qTable.txt', 'w')
        for state in sorted(self.table.keys()):
            fd.write(state + ' '),
            for action in sorted(self.table[state].keys(), reverse = True):
                fd.write(str(self.table[state][action][0])+' '),
            fd.write('\n')
        fd.close()

    def printPolicy(self):
        if self.numberOfQueues > 2:
            print "too many queues, cannnot print"
            return
        print '   ',
        for i in range(self.queueLen[0]+1):
            print '{:3s}'.format(str(i)),
        print ''
        for j in range(self.queueLen[1]+1):
            print '{:3s}'.format(str(j)),
            for k in range(self.queueLen[0]+1):
                state = str(k)+','+str(j)
                if self.findAction(state) == '100':
                    print '{:3s}'.format('+'),
                else:
                    if self.findAction(state) == '010':
                        print '{:3s}'.format('-'),
                    else:
                        print '{:3s}'.format('o'),
            print ''

    def printPolicyFile(self):
        fd = open("policy_qLearned.txt", 'w')
        for key in sorted(self.table.keys()):
            fd.write(key),
            fd.write(' '),
            fd.write(self.findAction(key))
            fd.write('\n')
        fd.close()



if __name__ == "__main__":
    queue0 = Queue(6,2)
    queue1 = Queue(6,5)
    queue2 = Queue(9,3)
    queue3 = Queue(8,3)
    queues = [queue0, queue1, queue2, queue3]
    qTable = QTable([x.totalLeng for x in queues])
    # qTable.doSomethingToTable()
    #agent = Agent(queues, qTable, 0.9, [0.4, 0.4], [5.0, 5.0], [[1, 3], [1,  3]])
    qTable.printPolicy()
    # print qTable.table
    # print len(qTable.table)
    raw_input("Press Enter to continue...")

    for e in range(50000):
        for q in queues:
            q.currentLeng = random.randrange(q.totalLeng+1)
        #agent = Agent(queues, qTable, 1- 1000.0/(e+1000.0), [0.45, 0.45], [5.0, 5.0], [[39, 0.05], [39, 0.1]])
        # agent = Agent(queues, qTable, 0.5, [0.45, 0.45], [5.0, 5.0], [[39, 0.05], [39, 0.1]])
        # agent = Agent(queues, qTable, 0.5, [0.2, 0.2, 0.2, 0.2], [7.0, 5.0, 5.0, 7.0], [[39, 0.05], [39, 0.15], [39, 0.08], [39, 0.05]])
        agent = Agent(queues, qTable, 0.5, [0.1, 0.2, 0.3, 0.25], [5.0, 5.0, 10.0, 10.0], [[39, 0.05], [20, 0.1], [39, 0.15], [10, 0.25]])
        if e%100 == 0:
            print "epoch {} started".format(e)
            print "initial state is {}".format(agent.currentState)
        # print "before q table:"
        # qTable.printTable()
        # q23.append(qTable.table['2,3']['010'][0])
        # print len(q23)
        for i in range(500):
            #print agent.currentState
            beforeState = agent.currentState
            agent.takeAction()
            afterState = agent.currentState
            # print "#############################"
            # print "before state is {}".format(beforeState)
            # print "after state is {}".format(afterState)
            # print "action taken is {}".format(agent.actionTaken)
            # print "one shot reward is {}".format(agent.reward)
            # print "epoch number is {}".format(agent.numberOfEpoch)
            # print "#############################"
            # print ""
            qTable.updateTable(beforeState, afterState, agent.actionTaken, agent.reward, agent.numberOfEpoch)
            # if (i%100 == 0):
            #     print "epoch number is {}".format(agent.numberOfEpoch)
            #qTable.printTable()
            #raw_input("Press Enter to continue...")
            # if beforeState == '5,6':
            #      qTable.printTable()
            #      print afterState
            #      print qTable.table[afterState]
            #      print agent.actionTaken
            #      raw_input("Press Enter to continue...")
    print "after q table:"
    qTable.printTable()
    qTable.printPolicy()
    qTable.printPolicyFile()
    qTable.printTableToFile()
    print "##########################################"
    # #
    # # for index, i in enumerate(qRecord):
    # #     print i
    # #     if index > 1000:
    # #         break
    # fd = open("2533_01000_qL_250_10.txt", 'w')
    # i = 0
    # while(1):
    #     try:
    #         fd.write(str(qRecord[i]))
    #         fd.write('\n')
    #         i += 1
    #     except:
    #         break;
    # fd.close()
    # fd = open("23010q_250_10_allstep.txt", 'w')
    # i = 0
    # while(1):
    #     try:
    #         fd.write(str(q23[i]))
    #         fd.write('\n')
    #         i += 1
    #     except:
    #         break;
    # fd.close()




        ##update Q table here!!







        #print agent.currentState
    # print agent.actionTaken
    #print qTable.table
    # for i in range(20):
    #     agent.takeAction()
    #     #print agent.action
    #     print agent.currentState
    #     print agent.reward
    # qTable = QTable([10,10])
    # print qTable.table
    # print len(qTable.table.keys())
