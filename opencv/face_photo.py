# -*- coding:utf-8 -*-
import cv2
import numpy as np

#读取图片
img = cv2.imread("../picture/test.jpg", cv2.IMREAD_UNCHANGED)

#BGR图像
# img[100:150, 400:500] = [255, 255, 0]

# 打印图片行数、列数、通道数
print(img.shape)
# 获取像素数目
print(img.size)
print(img.dtype)

#定义300*100矩阵 3对应BGR
face = np.ones((200, 200, 3))

#显示ROI区域
face = img[300:500, 300:500]
img[0:200,0:200] = face
cv2.imshow("face", img)

#等待显示
cv2.waitKey(0)
cv2.destroyAllWindows()
