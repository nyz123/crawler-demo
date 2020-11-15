#追赶法
import numpy as np
A=[[3.00000,2.00000,0.00000,0.00000],[-1.00000,3.00000,2.00000,0.00000],[0.00000,-1.00000,3.00000,2.00000],[0.00000,0.00000,-1.00000,3.00000]]
b=[[7.00000,11.00000,15.00000,9.00000]]

def get_base(A):#获得一个基，在上面修改得到答案
    base=list(np.zeros((len(A),len(A))))
    D=[]
    for i in base:
        D.append(list(i))
    return D

def get_gamma(A):#根据第一行公式γi=di
    base=get_base(A)
    for i in range(1,len(A)):
        base[i][i-1]=A[i][i-1]
    return base

def get_raw1(A,base):#根据第一行公式
    base[0][0]=A[0][0]
    base[0][1]=A[0][1]/base[0][0]
    return base

def get_other_raws(A,base,i):#递推后面几行
    base[i][i]=A[i][i]-A[i][i-1]*base[i-1][i]
    base[i][i+1]=A[i][i+1]/base[i][i]
    return base

def get_final_raw(A,base):#最后一行少一个β，另外求解，也可以和上面放在一起
    base[-1][-1]=A[-1][-1]-A[-1][-2]*base[-2][-1]
    return base

def get_all(A):#得到一个L和U并在一起的矩阵，由于U的主对角线为1，因此可以放在一起
    base=get_base(A)
    base=get_gamma(A)
    base=get_raw1(A,base)
    for i in range(1,len(A)-1):
        get_other_raws(A,base,i)
    get_final_raw(A,base)
    return base
    
def get_lower(A):#获得L
    for i in A:
        for j in i:
            if i.index(j)>A.index(i):
                A[A.index(i)][i.index(j)]=0
    return A

def get_upper(A):#获得U
    for i in A:
        for j in i:
            if i.index(j)<A.index(i):
                A[A.index(i)][i.index(j)]=0.0
            elif i.index(j)==A.index(i):
                A[A.index(i)][i.index(j)]=1.0
    return A

base=get_all(A)
lower=get_lower(base)
print(np.mat(lower).I*np.mat(b).T)#解得y
base=get_all(A)
upper=get_upper(base)
print(np.mat(upper).I*np.mat(lower).I*np.mat(b).T)#解得x
