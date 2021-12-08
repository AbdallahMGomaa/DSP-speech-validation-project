import numpy as np
from numpy.core.fromnumeric import argmin


def dtw(reference, sequence ,dist = np.linalg.norm, reconstruct=False):
    reference = np.array(reference)
    sequence = np.array(sequence)
    assert np.shape(reference)[1] == np.shape(sequence)[1],"reference and y must have the same number of columns"
    k = np.shape(reference)[1]
    r, c = np.shape(sequence)[0], np.shape(reference)[0]
    # assert r>=c//2 and r<=c*2, "reference must have at least half as many rows as sequence"
    if not (r>=c//2 and r<=c*2):
        # print("reference must have at least half as many rows as sequence")
        if reconstruct:
            return np.inf, None, None
        return np.inf

    # Initialize the cost matrix
    D = np.zeros((r+1,c+1))
    D[0, 1:] = np.inf
    D[1:, 0] = np.inf
    D[0,0] = 0

    # Initialize the distance matrix
    d = np.zeros((r,c))
    for i in range(r):
        for j in range(c):
            d[i,j] = dist(reference[j]-sequence[i])

    # setting unwanted region to infinity
    j_limit = 0
    for i in range(r):
        j_limit += 2
        for j in range(j_limit,c):
            d[i,j] = np.inf
    i_limit = 0
    for j in range(c):
        i_limit += 2
        for i in range(i_limit,r):
            d[i,j] = np.inf
    j_limit = c
    for i in reversed(range(r)):
        j_limit -= 2
        for j in reversed(range(j_limit)):
            d[i,j] = np.inf
    i_limit = r
    for j in reversed(range(c)):
        i_limit -= 2
        for i in reversed(range(i_limit)):
            d[i,j] = np.inf
    
    # initializing optimal path matrix
    B = np.zeros((r,c,2),dtype=np.int)
    B[0,0] = [0,0]

    # computing cost matrix and optimal path matrix
    for i in range(r):
        for j in range(c):
            if d[i,j] == np.inf:
                D[i+1,j+1] = np.inf
                continue
            if B[i-1,j,0] == i-2 and B[i-1,j,1] == j:
                D[i+1,j+1] = d[i,j]+min(D[i+1,j],D[i,j])
                index = argmin([D[i+1,j],D[i,j]])
                B[i,j] = [i-index,j-1]
            elif B[i,j-1,0] == i and B[i,j-1,1] == j-2:
                D[i+1,j+1] = d[i,j]+min(D[i,j],D[i,j+1])
                index = argmin([D[i,j+1],D[i,j]])
                B[i,j] = [i-1, j-index]
            else:
                D[i+1,j+1] = d[i,j]+min(D[i+1,j],D[i,j+1],D[i,j])
                index = argmin([D[i+1,j],D[i,j+1],D[i,j]])
                B[i,j] = [i-int(index>0), j-1+int(index==1)]
    

    if reconstruct:
        i = r-1
        j = c-1
        path = [(i,j)]
        while i>0 or j>0:
            step = (B[i,j,0],B[i,j,1])
            path.insert(0, (step[0],step[1]))
            i,j = step
        constructed_sequence = np.zeros((c,k))
        skipNext = False
        k=0
        for i,j in path:
            if not skipNext:
                if k+1<c and j == path[k+1][1]:
                    constructed_sequence[j] = (sequence[i]+sequence[i+1])/2
                    skipNext = True
                else:
                    constructed_sequence[j] = sequence[i]
            else:
                skipNext = False
            k += 1
        distances = np.zeros((c,1),np.float64)
        for i in range(c):
<<<<<<< HEAD
            distances[i] = np.sqrt((reference[i,:]-constructed_sequence[i,:]).T.dot(reference[i,:]-constructed_sequence[i,:]))        
=======
            distances[i] = np.sqrt((reference[i,:]-constructed_sequence[i,:]).T.dot(reference[i,:]-constructed_sequence[i,:]))
        
>>>>>>> 77ca8eccf2cd91b0c3cb8123493d8ab3f6dbe968
        return D[r,c],constructed_sequence, distances

    return D[r, c]