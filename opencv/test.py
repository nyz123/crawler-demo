# coding=utf-8

import cv2
import numpy as np

img = cv2.imread('../picture/test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imwrite('../picture/test_gray.jpg',gray)
cv2.imwrite('../picture/test_hsv.jpg',hsv)