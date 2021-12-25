import numpy as np
import matplotlib.pyplot as plt
def calculateThreshold(users,references,size=20,words=122):
    thresholds = np.zeros((words))
    for i in range(words//2):
        d11 = np.zeros((size))
        d12 = np.zeros((size))
        d21 = np.zeros((size))
        d22 = np.zeros((size))
        for j in range(size):
            d11[j] = users[j].utterences[2*i].distance(references[users[j].reference].utterences[2*i])
            d12[j] = users[j].utterences[2*i].distance(references[users[j].reference].utterences[2*i+1])
            d21[j] = users[j].utterences[2*i+1].distance(references[users[j].reference].utterences[2*i])
            d22[j] = users[j].utterences[2*i+1].distance(references[users[j].reference].utterences[2*i+1])
        thresholds[2*i] = np.mean(d11)/0.75
        thresholds[2*i+1] = np.mean(d22)/0.75
    return thresholds