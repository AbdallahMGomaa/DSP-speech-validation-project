import numpy as np
from numpy.core.fromnumeric import argmin

def dtw(reference, sequence , reconstruct=False):
    reference = np.array(reference)
    sequence = np.array(sequence)
    assert np.shape(reference)[1] == np.shape(sequence)[1],"reference and y must have the same number of columns"
    k = np.shape(reference)[1]
    r, c = np.shape(reference)[0], np.shape(sequence)[0]
    assert r>=c//2 and r<=c*2, "reference must have at least half as many rows as sequence"

    # Initialize the cost matrix
    D = np.zeros((r+1,c+1))
    D[0, 1:] = np.inf
    D[1:, 0] = np.inf
    D[0,0] = 0

    # Initialize the distance matrix
    d = np.zeros((r,c))
    for i in range(r):
        for j in range(c):
            d[i,j] = np.sqrt((reference[i]-sequence[j]).T.dot(reference[i]-sequence[j]))/k

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
    B = np.zeros((r+1, c+1,2),dtype=np.int)
    B[0,1:,:] = np.iinfo(np.int32).max
    B[1:,0,:] = np.iinfo(np.int32).max
    B[0,0,:] = [0,0]

    # computing cost matrix and optimal path matrix
    for i in range(r):
        for j in range(c):
            if d[i,j] == np.inf:
                D[i+1,j+1] = np.inf
                continue
            if B[i,j+1,0] == i-1 and B[i,j+1,1] == j+1:
                D[i+1,j+1] = d[i,j]+min(D[i+1,j],D[i,j])
                index = argmin([D[i,j],D[i+1,j]])
                B[i+1,j+1,0],B[i+1,j+1,1] = i+index,j
            elif B[i+1,j,0] == i+1 and B[i+1,j,1] == j-1:
                D[i+1,j+1] = d[i,j]+min(D[i,j],D[i,j+1])
                index = argmin([D[i,j],D[i,j+1]])
                B[i+1,j+1,0],B[i+1,j+1,1] = i, j+index
            else:
                D[i+1,j+1] = d[i,j]+min(D[i+1,j],D[i,j+1],D[i,j])
                index = argmin([D[i+1,j],D[i,j+1],D[i,j]])
                B[i+1,j+1,0],B[i+1,j+1,1] = i+int(index==0), j+int(index==1)
    i = r
    j = c
    path = np.zeros((c,2),dtype=np.int)
    while i>1 and j>1:
        path[j-1] = np.flip(B[i,j],0)
        path[j-1,1] -= 1
        i,j = B[i,j,0],B[i,j,1]

    if reconstruct:
        constructed_sequence = np.zeros((c,k))
        for i,j in path:
            constructed_sequence[i] = sequence[j]
        return D[r,c],constructed_sequence
    return D[r, c],path

