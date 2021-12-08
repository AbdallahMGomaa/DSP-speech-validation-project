import numpy as np
def calculateThreshold(users,references,size=20,pairs=61):
    thresholds = np.zeros((pairs))
    for i in range(pairs):
        dist1 =np.zeros((size))
        dist2 = np.zeros((size))
        for j in range(size):
            dist1[j] = users[j].utterences[2*i].distance(references[users[j].reference].utterences[2*i])
            dist2[j] = users[j].utterences[2*i+1].distance(references[users[j].reference].utterences[2*i+1])
            thresholds[i] = (np.mean(dist1)+np.mean(dist2))/2
    return thresholds