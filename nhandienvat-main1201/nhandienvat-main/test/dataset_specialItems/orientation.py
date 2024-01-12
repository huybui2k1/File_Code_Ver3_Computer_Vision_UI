from __future__ import print_function
from __future__ import division
import cv2 as cv
import numpy as np
import argparse
from math import atan2, cos, sin, sqrt, pi
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def drawAxis(img, p_, q_, colour, scale,degree):
 p = list(p_)
 q = list(q_)
 print("diemP: ",p)
 print("diemQ: ",q)
 text1 = f"({p[0]}, {p[1]})"
 
#  cv.putText(img, text1, (p[0]+30,p[1]+30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
 angle = atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
 print("angle: ",degree)
 text2 = f"{round(degree,2)} degree"
 cv.putText(img, text2, (p[0]+10,p[1]-30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

 hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
 # Here we lengthen the arrow by a factor of scale
 q[0] = p[0] - scale * hypotenuse * cos(angle)
 q[1] = p[1] - scale * hypotenuse * sin(angle)
 cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)
 # create the arrow hooks
 p[0] = q[0] + 9 * cos(angle + pi / 4)
 p[1] = q[1] + 9 * sin(angle + pi / 4)
 cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)
 p[0] = q[0] + 9 * cos(angle - pi / 4)
 p[1] = q[1] + 9 * sin(angle - pi / 4)
 cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)
 
def getOrientation(pts, img):
 sz = len(pts)
 data_pts = np.empty((sz, 2), dtype=np.float64)
 for i in range(data_pts.shape[0]):
  data_pts[i,0] = pts[i,0,0]
  data_pts[i,1] = pts[i,0,1]
 # Perform PCA analysis
 mean = np.empty((0))
 mean, eigenvectors, eigenvalues = cv.PCACompute2(data_pts, mean)
 # Store the center of the object
 cntr = (int(mean[0,0]), int(mean[0,1]))
 
 
 cv.circle(img, cntr, 2, (255, 0, 255), 1)
 p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
 p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
#  cv.circle(img, (eigenvectors[0,1], eigenvectors[0,0]), 2, (0, 0, 255), 1)
 angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
 degree = angle * (180 / np.pi)

 drawAxis(img, cntr, p1, (0, 255, 0), 2,degree)
 drawAxis(img, cntr, p2, (255, 255, 0), 5,degree)
 return degree

#  //////////////////////////////MAIN//////////////////////////////////////////////
# parser = argparse.ArgumentParser(description='Code for Introduction to Principal Component Analysis (PCA) tutorial.\
#  This program demonstrates how to use OpenCV PCA to extract the orientation of an object.')
# parser.add_argument('--input', help='Path to input image.', default='pca_test1.jpg')
# args = parser.parse_args()
# src = cv.imread(cv.samples.findFile(args.input))

# image = cv.imread(r"E:\My_Code\NhanDienvat\detectByYolov8\dataset_specialItems\train\images\20230922_154848_jpg.rf.6029095e75735d85f1bc5d292e834e12.jpg")

image = cv.imread(r"E:\My_Code\NhanDienvat\detectByYolov8\dataset_specialItems\train\images\20230922_155254_jpg.rf.53417c933aae3540eb4f59ccc6e42b39.jpg")


# Giảm độ sáng của ảnh (có thể điều chỉnh giá trị beta để giảm hoặc tăng độ sáng)
beta = -50  # Giảm độ sáng

# Sử dụng hàm cv2.convertScaleAbs để giảm độ sáng của ảnh
src = cv.convertScaleAbs(image, alpha=1, beta=beta)


# Check if image is loaded successfully
if src is None:
 print('Could not open or find the image: ', args.input)
 exit(0)
cv.imshow('src', src)
# Convert image to grayscale
gray_picture = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

gray_inverted = cv.bitwise_not(gray_picture)
# Convert image to binary
_, bw = cv.threshold(gray_picture, 50, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
contours, _ = cv.findContours(bw, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
for i, c in enumerate(contours):
 # Calculate the area of each contour
 area = cv.contourArea(c)
 # Ignore contours that are too small or too large
 if area < 1e2*3 or 1e5 < area:
  continue
 # Draw each contour only for visualisation purposes
 cv.drawContours(src, contours, i, (0, 0, 255), 2)
 # Find the orientation of each shape
 getOrientation(c, src)
 cv.imwrite('orientation_image.jpg',src)
cv.imshow('output', src)
# Assuming you have a grayscale image in the 'gray_picture' variable
# Normalize the grayscale values to be between 0 and 1

plt.imshow(bw, cmap="gray")
plt.title("Bitwise Gray")
plt.axis("off")
plt.show()

plt.imshow(gray_inverted, cmap="gray")
plt.title("gray_inverted Gray")
plt.axis("off")
plt.show()

cv.waitKey()