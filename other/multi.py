import numpy as np

A = [
    [2,-1,0,0,0,0],
    [-1,3,-2,0,0,0],
    [0,-1,2,-1,0,0],
    [0,0,-3,5,2,0],
    [0,0,0,1,3,2],
    [0,0,0,0,-2,1],
]
# X = [3,2,1,5,1,2]
X = [2,4,7,6,1,2]
Y = [4,3,-3.8,14.5,6.2,5.63636364]
U = [
    [ 2,-1, 0, 0, 0, 0],
    [ 0, 2.5,-2, 0, 0, 0],
    [ 0, 0, 1.2,-1, 0, 0],
    [ 0, 0, 0, 2.5,2, 0],
    [ 0, 0, 0, 0, 2.2, 2],
    [ 0, 0, 0, 0, 0, 2.81818182]
]

def getMulti(A,X):
    num = len(A)
    res = np.zeros((num))
    for i in range(num):
        for j in range(num):
            res[i]+=A[i][j] * X[j]

    return res



if __name__ == '__main__':
    # print(getMulti(U,X))
    print(getMulti(A,X))
