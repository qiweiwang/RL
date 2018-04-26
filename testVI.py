from valueIteration import *

if __name__ == "__main__":
    stateSpaceList = findAllStates([6,6])
    stateSpace = []
    for stateList in stateSpaceList:
        stateSpace.append(listToState(stateList))

    vi = valueIterator(stateSpace, ['100', '010', '001'], 0.95, [0.45, 0.45])
    print vi.eReward('6,0', '010')
