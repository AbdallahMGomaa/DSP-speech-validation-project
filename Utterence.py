# from fastdtw import dtw as dtw
from dtw import dtw
from scipy.spatial.distance import euclidean
# import numpy as np


class Utterence:
    def __init__(self,pair,word,MFCC) -> None:
        self.pair = pair
        self.word = word
        self.MFCC = MFCC
        self.perFrameDistance = None
        self.reconstructed = None
        self.predicted = -1
    def distance(self,reference):
        # shape = np.shape(reference.MFCC)
        d = dtw(reference.MFCC,self.MFCC,False)
        # d, path = dtw(reference.MFCC,self.MFCC, euclidean)
        # self.reconstructed = np.zeros(shape)
        # for i,j in enumerate(path):
        #     self.reconstructed[i] = self.MFCC[j]
        # self.totalDistance = d
        # dist = []
        # for i in range(np.shape(reference.MFCC)[0]):
        #     dist.append(euclidean(reference.MFCC[i],self.reconstructed[i]))
        # self.perFrameDistance = dist
        return d

    def reconstruct(self,reference):
        d,self.reconstructed,distances = dtw(reference.MFCC,self.MFCC,True)
        return d,self.reconstructed,distances
        