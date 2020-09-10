# -*- coding:utf-8 -*-
import cv2
import numpy as np
import math

X0 = 20


def is_on_arc(p):
    # d  =  r- ( [r/x0+1] * 2pi-arctany/x ) * x0 / 2pi
    # 0<d<4 
    # r=sqrt(x^+y^)
    r = math.sqrt(math.pow(p[0],2)+math.pow(p[1],2))
    arc = math.atan(p[1]/p[0])
    d = r - ((math.floor(r/X0 + 1) * 2 * math.pi - arc) * X0 /(2*math.pi))
    return d>=0 and d<= 4

def get_data():
    #读取图片
    src = cv2.imread("../picture/niu.jpg", cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    rows, cols, chn = src.shape
    D = min(rows,cols)
    R = math.floor(D/2)
    point = [rows/2,cols/2]

    v = 20

    print('高，列：',rows,cols,chn,R)
    print(img[0,0])

    for i in range(0,rows):
        for j in range(0,cols):
            dis = math.sqrt(math.pow(i-point[0],2)+math.pow(j-point[1],2))
            remainder = dis%20
            if(dis > R or remainder>10):
                img[i,j] = 255


    # cv2.imshow("wenxiang", img)

    cv2.imwrite('../picture/wenxiang.jpg',img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ =='main':
    get_data()
