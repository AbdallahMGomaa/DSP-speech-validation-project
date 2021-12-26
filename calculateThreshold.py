import numpy as np
import matplotlib.pyplot as plt
def calculateThreshold(users,references,words=122):
    size = len(users)
    d = np.zeros((size*words))
    k = 0
    for i in range(words//2):
        for j in range(size):
            d[k] = users[j].utterences[2*i].distance(references[users[j].reference].utterences[2*i])
            d[k+1] = users[j].utterences[2*i+1].distance(references[users[j].reference].utterences[2*i+1])
            k = k+2
    d = d[d!=np.inf]
    threshold = max(d)
    return threshold