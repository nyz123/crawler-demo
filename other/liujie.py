import math
import numpy as np

NUM = 6
A = [
    [3,2,0,0,0,0],
    [-1,3,2,0,0,0],
    [0,-1,3,2,0,0],
    [0,0,-1,3,2,0],
    [0,0,0,-1,3,2],
    [0,0,0,0,-1,3],
]
D = [7,11,15,9,1,8]

def get_base(A):#获得一个基，在上面修改得到答案
    base=list(np.zeros((len(A),len(A))))
    D=[]
    for i in base:
        D.append(list(i))
    return D

def getLU(A):
    L = np.zeros((NUM,NUM))
    U = np.zeros((NUM,NUM))
    # Ui = bi - LiCi-1
    # Li = ai / Ui-1
    # U1 = b1
    # 计算L U
    U[0][0] = A[0][0]
    for i in range(NUM):
        L[i][i] = 1
        if(i != (NUM-1)):
            U[i][i+1] = A[i][i+1]
        if(i != 0):
            L[i][i-1] = A[i][i-1]/ U[i-1][i-1]
            U[i][i] = A[i][i] - L[i][i-1] * A[i-1][i]
    return [L,U]

def getY(D,L):
    # y1 = d1
    # yi = di - Liyi-1
    Y = np.zeros((NUM))
    Y[0] = D[0]
    for i in range(1,NUM):
        Y[i] = D[i] - L[i][i-1]*Y[i-1]
    return Y

def getX(A,U,Y):
    # Xi = (Yi-CiXi+1)/Ui
    # X6 = Y6/U6
    X = np.zeros((NUM))
    X[NUM-1] = Y[NUM-1]/U[NUM-1][NUM-1]
    for i in range(NUM-2,-1,-1):
        X[i] = (Y[i]-A[i-1][i]*X[i+1])/U[i][i]
    return X

def calc(A,D):
    lu = getLU(A)
    L = lu[0]
    U = lu[1]
    # print('L:',L)
    # print('U:',U)
    Y = getY(D,L)
    # print(Y)
    X = getX(A,U,Y)
    print(X)
    return 

if __name__ == '__main__':
    calc(A,D)