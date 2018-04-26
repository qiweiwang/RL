import copy
import numpy as np

##############################utility functions#############################
def findAllActions(numberOfQueues):
    actionList = []
    for j in range(numberOfQueues+1):
        action = ''
        for i in range(numberOfQueues+1):
            if i == j:
                action = action + '1'
            else:
                action = action + '0'
        actionList.append(action)
    return actionList

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

def stateToList(stateStr):
    stateStrSplit = stateStr.split(',')
    stateParsed = []
    for state in stateStrSplit:
        stateParsed.append(int(state))
    return stateParsed

def listToState(stateParsed):
    stateStr = ''
    for state in stateParsed:
        stateStr = stateStr + str(state) + ','
    stateStr = stateStr[:-1]
    return stateStr

def actionToArray(actionString):
    action = []
    for i in actionString:
        action.append(int(i))
    action = np.array(action)
    return action

def arrayToAction(actionArray):
    actionString = ''
    for i in actionArray.tolist():
        actionString = actionString + str(i)
    return actionString
