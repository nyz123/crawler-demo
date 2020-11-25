#encoding:utf-8
import cv2
filename = "/users/Downloads/20181102142518.png"
def detect(filename):
 # haarcascade_frontalface_default.xml存储在package安装的位置
face_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_default.xml")
 img = cv2.imread(filename)
 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 #传递参数是scaleFactor和minNeighbors,分别表示人脸检测过程中每次迭代时图像的压缩率以及每个人脸矩形保留近邻数目的最小值
 #检测结果返回人脸矩形数组
 #python学习资料交流分享群：852 250 729
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x, y, w, h) in faces:
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.namedWindow("Human Face Result!")
    cv2.imshow("Human Face Result!", img)
    cv2.imwrite("images/Face.jpg", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    detect(filename)