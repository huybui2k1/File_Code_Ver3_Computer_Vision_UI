import cv2
import numpy as np

def apply_min_area(contour):
 contour = np.array(contour, dtype=np.int32)
 rotated_rect= cv2.minAreaRect(contour)
 #lấy góc mặc định
 #lấy tọa độ các đỉnh của rotated_rect
 rect_points = cv2.boxPoints(rotated_rect).astype(int)

 edge1 = np.array(rect_points[1]) - np.array(rect_points[0])
 edge2 = np.array(rect_points[2]) - np.array(rect_points[1])
 reference = np.array([1, 0])
#  với ta có adge1 và edge2 là toa độ lần lượt của vecto 01 và vecto 12
#  và cùng với cú pháp numpy np.linalg.norm(edge) ta sẽ tính được độ dài của 2 vecto đó, độ dài nào lớn hơn(vì đây là hình chữ nhật và ta lấy cạnh dài để căn góc) thì 
#  được dùng làm đoạn thẳng kết hợp với điểm tham chiếu để tính toán góc bằng công thức cosin
#  print("dodai: ",np.linalg.norm(edge1),np.linalg.norm(edge2))
#  print("point: ", rect_points)
 if np.linalg.norm(edge1) > np.linalg.norm(edge2):    

         used_edge = edge1
         #  np.arccos dùng để tính phép tính arccos trong lượng giác, np.dot dùng để tính tích vô hướng
         angle = (180.0 / np.pi) * (np.arccos(np.dot(reference, used_edge) / (np.linalg.norm(reference) * np.linalg.norm(used_edge))))
         angle = 360 - angle
        #  angle = 180 - pre_angle
        #  print("angle AS: ",angle)    
 else:
         
         used_edge = edge2
         angle = (180.0 / np.pi)*(np.arccos(np.dot(reference, used_edge) / (np.linalg.norm(reference) * np.linalg.norm(used_edge))))
        #  print("angle AC: ",angle)
#  if angle > 180:
#         angle = 180 - (360 - abs(angle))
 return angle
