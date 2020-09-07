# -*- coding:utf-8 -*-
import cv2
import numpy as np

#读取图片
img = cv2.imread("../picture/niu.jpg", cv2.IMREAD_UNCHANGED)
rows, cols, chn = img.shape
r = min(rows,cols)/2
print('高，列：',rows,cols,chn,r)
# for i in r:    
    # x = np.random.randint(0, rows) 
    # y = np.random.randint(0, cols)    
    # img[x,y,:] = 255


cv2.imshow("蚊香画", img)
           
#等待显示
cv2.waitKey(0)
cv2.destroyAllWindows()
