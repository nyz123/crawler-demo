# coding=utf-8

import cv2
import numpy as np

img = cv2.imread('../picture/niu.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("Demo", gray)
k=cv2.waitKey(0)
if k==27:
    cv2.destroyAllWindows()

cv2.imwrite('../picture/niu_gray.jpg',gray)

# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# cv2.imwrite('../picture/test_hsv.jpg',hsv)