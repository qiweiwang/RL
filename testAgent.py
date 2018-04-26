from learnTx import *
import os


if __name__ == "__main__":

    queue0 = Queue(6,2)
    queue1 = Queue(6,3)
    queues = [queue0, queue1]
    qTable = QTable([queue0.totalLeng, queue1.totalLeng])

    total = 0
    for i in range(10000):
        queue0 = Queue(6,6)
        queue1 = Queue(6,0)
        queues = [queue0, queue1]
        qTable = QTable([queue0.totalLeng, queue1.totalLeng])
        agent = Agent(queues, qTable, 1, [0.45, 0.45], [5.0, 5.0], [[39, 0.05], [39, 0.1]])
        beforeState = agent.currentState
        agent.takeAction()
        afterState = agent.currentState
        # print "beforeState is: {}".format(beforeState)
        # print "afterState is: {}".format(afterState)
        # print "action taken is: {}".format(agent.actionTaken)
        # print "instant reward is: {}".format(agent.reward)
        # raw_input()
        # print agent.reward
        total += agent.reward
    total /= 10000
    print total

    os.system('python testVI.py')
