import numpy as np
from sklearn.preprocessing import StandardScaler
def scale(users,references):
    mfccs = []
    for i in range(len(references)):
        for j in range(len(references[i].utterences)):
            for k in range(len(references[i].utterences[j].MFCC)):
                mfccs.append(references[i].utterences[j].MFCC[k])
    for i in range(len(users)):
        for j in range(len(users[i].utterences)):
            for k in range(len(users[i].utterences[j].MFCC)):
                mfccs.append(users[i].utterences[j].MFCC[k])
    mfccs = np.array(mfccs).reshape((len(mfccs),len(mfccs[0])))
    scaler = StandardScaler()
    scaler.fit(mfccs)
    for i in range(len(references)):
        for j in range(len(references[i].utterences)):
            references[i].utterences[j].MFCC = scaler.transform(references[i].utterences[j].MFCC)
    for i in range(len(users)):
        for j in range(len(users[i].utterences)):
            users[i].utterences[j].MFCC = scaler.transform(users[i].utterences[j].MFCC)
    return users,references

