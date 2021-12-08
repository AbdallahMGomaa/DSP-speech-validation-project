from calculateJudgements import *

def calculateThreshold(users,references,size=20):
    assert len(users)>= size
    allWordsDistances = []
    pairs = len(users[0].utterences)//2
    for j in range(pairs):
        wordDistances = [[],[]]
        for i in range(len(users)):
            wordDistances[0].append(users[i].utterences[j*2].distance(references[i].utterences[j*2]))
            wordDistances[0].append(users[i].utterences[j*2+1].distance(references[i].utterences[j*2+1]))
        allWordsDistances.append(wordDistances)
    thresholds = []
    
    return thresholds
        