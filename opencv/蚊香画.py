# -*- coding:utf-8 -*-
import cv2
import numpy as np
import math

# 定义变量
X0 = 20
PI = math.pi
W_white = W_black = 4
path = 'e:\\xie\\crawler-demo\\picture\\niu.jpg'

def get_distance(p1,p2):
    return math.sqrt(math.pow(p1[0]-p2[0],2)+math.pow(p1[1]-p2[1],2))

def is_on_arc1(p):
    dis = get_distance([0,0],p)
    if p[0]==0:
        return False
    arc = math.atan(p[1]/p[0])
    res = dis + arc*X0/(2*PI) - X0*math.floor(dis/X0+1)
    return res<=W_white and res>=W_white*(-1)

def is_on_arc(p):
    r = get_distance([0,0],p)
    if p[0]==0:
        if p[1]>0:
            arc = 0.5*PI
        elif p[1]<=0:
            arc = -0.5*PI
        else:
            arc = 0
    else:
        arc = math.atan(p[1]/p[0])
    if arc>0 and p[0]<0:  
        arc = PI + arc
    elif arc < 0 and p[0]<0:
        arc = PI + arc
    elif arc < 0 and p[0]>0:
        arc = 2 * PI +arc

    res = r - X0 * (math.floor(r/X0) + arc/(2*PI)) 
    return res>=-1 * W_white and res<=W_white


def get_data():
    #读取图片
    src = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    rows, cols, chn = src.shape
    D = min(rows,cols)
    R = math.floor(D/2)
    point = [math.floor(rows/2),math.floor(cols/2)]

    print('高，列：',rows,cols,chn,R)
    print(point,R,math.floor(point[0]-R),math.floor(point[0]+R),math.floor(point[1]-R),math.floor(point[1]+R))
    
    for i in range(math.floor(point[0]-R),math.floor(point[0]+R)):
        for j in range(math.floor(point[1]-R),math.floor(point[1]+R)):
            y = int(i - point[0])
            x = int(j - point[1])
            if(get_distance([0,0],[x,y])<=R and is_on_arc([x,y])):
                img[i,j] = 255

    cv2.imshow("wenxiang", img)

    cv2.imwrite('e:\\xie\\crawler-demo\\picture\\wenxiang.jpg',img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    get_data()
