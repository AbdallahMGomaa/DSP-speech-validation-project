import numpy as np
def calculateThreshold(users,references,words=122):
    userSize = len(users)
    thresholds = np.zeros((words))
    for j in range(words//2):
        d11 = np.zeros((userSize))
        d12 = np.zeros((userSize))
        d21 = np.zeros((userSize))
        d22 = np.zeros((userSize))
        k = 0
        for i in range(userSize):
            d11[k] = users[i].utterences[j*2].distance(references[users[i].reference].utterences[j*2])
            d22[k] = users[i].utterences[j*2+1].distance(references[users[i].reference].utterences[j*2+1])
            k += 1
        d11 = d11[d11!=np.inf]
        d12 = d12[d12!=np.inf]
        d21 = d21[d21!=np.inf]
        d22 = d22[d22!=np.inf]
        thresholds[2*j] = np.mean(d11)/0.6
        thresholds[2*j+1] = np.mean(d22)/0.6
        # thresholds[2*j] = np.inf
        # thresholds[2*j+1] = np.inf
    return thresholds