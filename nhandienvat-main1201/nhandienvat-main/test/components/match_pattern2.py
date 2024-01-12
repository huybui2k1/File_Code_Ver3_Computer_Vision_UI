import cv2 
from ultis.rotate_template import rotate_template 
import numpy as np


def match_template(img_gray, rotated_template,mask,method,angle,scale,threshold):
   method = eval(method)

#    if (img_gray.shape[0] < rotated_template.shape[0]) or (img_gray.shape[1] < rotated_template.shape[1]):
#         return
   matched_points = cv2.matchTemplate(rotated_template,img_gray, method, None)
   _, max_val, _, max_loc = cv2.minMaxLoc(matched_points)
   print("max val: ",max_val)
   if max_val >= threshold and max_val <= 1.0:
    #  return [*max_loc, angle, scale, max_val]
     return max_val
      


def match_pattern2(temp_gray, img_gray, bbox, angle, method, threshold):
    h,w = temp_gray.shape[:2]
    height_bb, width_bb = bbox[3] ,bbox[2] 
    img_padded = cv2.copyMakeBorder(temp_gray, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=0)
    height_temp, width_temp = img_padded.shape[:2]
    ctr_y,ctr_x = height_temp//2, width_temp//2
    print("tama: ",ctr_x,ctr_y)
    cv2.circle(temp_gray, (ctr_x,ctr_y), 1, (0,0,255))
    rotation_matrix = cv2.getRotationMatrix2D((ctr_x ,ctr_y), -angle , 0.6)
    cos, sin = abs(rotation_matrix[0, 0]), abs(rotation_matrix[0, 1])
    newW = int((h * sin) + (w * cos))
    newH = int((h * cos) + (w * sin))
     # calculate new rotation center
    rotation_matrix[0, 2] += (newW / 2) 
    rotation_matrix[1, 2] += (newH / 2) - ctr_y - 10
    rotated_tmp = cv2.warpAffine(temp_gray, rotation_matrix, (newW, newH),borderValue=(0, 0, 0), flags=cv2.INTER_LINEAR)
    # Tạo một mảng điểm ảnh trắng với kích thước bằng với ảnh xám
    mask = np.full_like(temp_gray, 255, dtype=np.uint8)
# Áp dụng biến đổi affine cho mask
    rotated_mask = cv2.warpAffine(mask, rotation_matrix, (width_temp, height_temp), borderValue=(0, 0, 0), flags=cv2.INTER_LINEAR)
    point = match_template(img_gray, rotated_tmp,mask,method,angle,100,threshold)
    cv2.imwrite("xoay_temp.jpg",rotated_tmp)
    cv2.imwrite("xoay_temp2.jpg",rotated_mask)
    return point
    