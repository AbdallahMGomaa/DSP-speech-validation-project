import numpy as np
import matplotlib.pyplot as plt
def calculateThreshold(users,references,size=20,words=122):
    thresholds = np.zeros((words))
    for i in range(words//2):
    #     d11 = np.zeros((size))
    #     d12 = np.zeros((size))
    #     d21 = np.zeros((size))
    #     d22 = np.zeros((size))
    #     for j in range(size):
    #         d11[j] = users[j].utterences[2*i].distance(references[users[j].reference].utterences[2*i])
    #         d12[j] = users[j].utterences[2*i].distance(references[users[j].reference].utterences[2*i+1])
    #         d21[j] = users[j].utterences[2*i+1].distance(references[users[j].reference].utterences[2*i])
    #         d22[j] = users[j].utterences[2*i+1].distance(references[users[j].reference].utterences[2*i+1])
    #     d11 = d11[d11!=np.inf]
    #     d12 = d12[d12!=np.inf]
    #     d21 = d21[d21!=np.inf]
    #     d22 = d22[d22!=np.inf]

        # thresholds[2*i] = (np.mean(d11)+np.mean(d12))/2
        # thresholds[2*i+1] = (np.mean(d21)+np.mean(d22))/2
        thresholds[2*i] = np.inf
        thresholds[2*i+1] = np.inf
        
    return thresholds