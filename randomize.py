import sys
import numpy as np


#randomly choose a index from distribution
def randomChoose_cmf(cmf):
    if abs(cmf[-1]-1) < 0.00000001:
        r = np.random.random()
        for i in cmf:
            if r < i:
                return cmf.index(i)
    else:
        print 'randomChoose: invalid CMF'


def randomChoose(distribution):
    cmf = []
    c = 0
    for i, dis in enumerate(distribution):
        c = c + dis
        cmf.append(c)
    #print cmf
    return randomChoose_cmf(cmf)

if __name__ == '__main__':
    print randomChoose_cmf([0.2,0.5,1])
    print randomChoose([0.2,0.3,0.1])
