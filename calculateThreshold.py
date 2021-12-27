import numpy as np
def calculateThreshold(users,references,words=122):
    refSize = len(references)
    userSize = len(users)
    thresholds = np.zeros((words))
    d = np.zeros((userSize*(words-1)*refSize))
    for i in range(words):
        m = 0
        for j in range(userSize):
            for l in range(refSize):
                for k in range(words):
                    if k != i:
                        d[m] = users[j].utterences[i].distance(references[l].utterences[k])
                        m += 1
        d = d[d!=np.inf]
        thresholds[i] = np.mean(d)
    return thresholds