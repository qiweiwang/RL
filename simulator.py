import numpy as np
import sys
import copy
import math

from queue import Queue
import randomize as rnd


# # one shot one queue simulator
# class SimpleSimulator:
#
#     reward = 0
#     arr_p = 1.0
#     snr = 5.0
#
#     #constructor
#     #def __init__(self):
#
#
#     #get simulation result
#     #first dequeue, then enqueue
#     #check queue length > 0 before use
#     def sim(self, queue_before, policy):
#         self.action = [0,0]
#         self.queue_before = queue_before
#         self.queue_after =  copy.copy(queue_before)
#         #send or not send
#         if np.random.random() < policy[0]:
#             self.queue_after.de()
#             self.action[0] = 1
#         else:
#             self.action[0] = 0
#         # admit or not admit
#         if np.random.random() < self.arr_p:
#             if np.random.random() < policy[1]:
#                 self.queue_after.en()
#                 self.action[1] = 1
#         self.reward = self.insReward(self.action, self.snr, self.queue_after)
#
#     def insReward(self, action, snr, queue):
#         #thruput reward
#         rwd_thu = action[1]
#         rwd_leng = self.queue_after.currentLeng*(-1)
#         rwd_cost = -1/snr*action[0]
#         return rwd_thu+rwd_cost+rwd_leng



# one shot multiQueue simulator
# v1: for a fixed snr matrix




class MultiSimulator:

    def __init__(self, arr_p, snr, weight):
        if len(arr_p) == len(snr):
            self.arr_p = arr_p
            self.snr = snr
            self.numberOfQueues = len(arr_p)
            self.weight = weight
        else:
            print 'MultiSimulator: size does not match'

    # return all queue status after one shot, tx-only policy. And sum of all queue reward
    def simTx(self, queues, tx_policy):
        txPolicy = tx_policy.tolist()
        txQueueIndex = rnd.randomChoose(txPolicy)
        oneShotReward = 0
        action = []
        for i in range(self.numberOfQueues):
            action.append(0)
            if i == txQueueIndex:
                action[i] = 1
            reward = self.simpleTxSim(queues[i], action[i], self.arr_p[i], self.snr[i], self.weight[i])
            oneShotReward = oneShotReward + reward
        return [oneShotReward, action]

    # one queue sim for only tx policy
    def simpleTxSim(self, queue, action, arr_p, snr, weight):
        queue_before = copy.copy(queue)
        if action == 1:
            queue.de()
        rwd_cost = -1/snr*(queue_before.currentLeng - queue.currentLeng)
        #print "cost is {}".format(rwd_cost)
        # print snr
        # print (queue_before.currentLeng - queue.currentLeng)
        queue_before = copy.copy(queue)
        if np.random.random()<arr_p:
            queue.en()
            #print "enqueue"
        rwd_thu = (queue.currentLeng - queue_before.currentLeng)*weight[0]
        #print "thruput reward is {}".format(rwd_thu)
        rwd_dly = -1*math.exp(queue.currentLeng)*weight[1]
        #print "delay cost is {}".format(rwd_dly)
        #print "######"

        return rwd_thu+rwd_dly+rwd_cost

    # return all queue status after one shot, and sum of all queue reward
    def sim(self, queues, ad_policy, tx_policy):
        adPolicy = ad_policy.tolist()
        txPolicy = tx_policy.tolist()
        #queues_before = queues
        #queues_after = queues
        txQueueIndex = rnd.randomChoose(txPolicy)
        adQueueIndex = rnd.randomChoose(adPolicy)
        #txQueueIndex = rnd.randomChoose(tx_policy)
        # print 'ad is {}'.format(adQueueIndex)
        # print 'tx is {}'.format(txQueueIndex)
        oneShotReward = 0
        action = []
        for i in range(self.numberOfQueues):
            action.append([0,0])
            if i == adQueueIndex:
                if np.random.random()<self.arr_p[i]:
                    action[i][0] = 1
            if i == txQueueIndex:
                action[i][1] = 1
            simpleReward = self.simpleSim(queues[i], action[i], self.snr[i], self.weight[i])
            oneShotReward = oneShotReward + simpleReward

        return [oneShotReward, action]

    #return one queue status and reward given a deterministic action
    def simpleSim(self, queue, action, snr, weight):
        queue_before = copy.copy(queue)
        if action[1] == 1:
            queue.de()
        if action[0] == 1:
            queue.en()

        #one queue, instant reward
        rwd_thu = weight[0]*(queue.currentLeng - queue_before.currentLeng)
        rwd_dly = -1*queue.currentLeng*weight[1]
        rwd_cost = -1/snr*action[1]
        return rwd_thu+rwd_dly+rwd_cost


if __name__ == '__main__':
    testQueue0 = Queue(6,3)
    testQueue1 = Queue(6,5)
    testQueues = [testQueue0, testQueue1]

    print 'previous queue 0 length is {}'.format(testQueue0.currentLeng)
    print 'previous queue 1 length is {}'.format(testQueue1.currentLeng)

    simulator = MultiSimulator([0.8,0.4], [10.0, 5.0], [[0.7, 0.3], [0.3, 0.7]])
    [reward, action] = simulator.sim_tx(testQueues, np.array([0,1]))

    print 'after simulation'
    print 'queue 0 length is {}'.format(testQueues[0].currentLeng)
    print 'queue 1 length is {}'.format(testQueues[1].currentLeng)
    print 'reward is {}'.format(reward)
    print 'action taken is'
    print action




    # print testQueue.currentLeng
    # oneStepSim = SimpleSimulator()
    # print oneStepSim.arr_p
    # oneStepSim.sim(testQueue, [0.3,0.2])
    # print 'previous length is {}'.format(oneStepSim.queue_before.currentLeng)
    # print oneStepSim.queue_after.currentLeng
    # print oneStepSim.reward
