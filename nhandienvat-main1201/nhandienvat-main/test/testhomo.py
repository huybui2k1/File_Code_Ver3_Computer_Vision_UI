import numpy as np
import cv2


center = np.array([[2083, 420]])
center = np.hstack((center, np.ones((center.shape[0], 1)))).T
# # Nạp ma trận homography từ tệp tin .npy
homography_matrix = np.load(r'C:\Users\TKD01A-1\Desktop\Projects\nachi_prog\Computer_vision\nhandienvat-main\nhandienvat-main\test\homography_matrix.npy')
# print("matrix: ",homography_matrix)
transformed_point = np.dot(homography_matrix, center)
# Chia cho phần tử cuối cùng để có tọa độ (x, y, 1)
transformed_point = transformed_point / transformed_point[2]
center_point = transformed_point[:2].T
# print("result convert: ",center_point)
result = (center_point[:,0],center_point[:,1] )
print('result: ',result)
# return transformed_point[0], transformed_point[1]
