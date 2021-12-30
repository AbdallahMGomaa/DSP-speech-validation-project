import numpy as np
def calculateThreshold(users,references,words=122):
    refSize = len(references)
    userSize = len(users)
    thresholds = np.zeros((words))
    for i in range(userSize):
        for j in range(words//2):
            d11 = users[i].utterences[j*2].distance(references[users[i].reference].utterences[j*2])
            d22 = users[i].utterences[j*2+1].distance(references[users[i].reference].utterences[j*2+1])
    d11 = d11[d11!=np.inf]
    d22 = d22[d22!=np.inf]
    thresholds[i] = (np.mean(d11)+np.mean(d22))*0.6
    return thresholds