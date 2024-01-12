import cv2
import numpy as np

def rotate_object(temp_image, angle):
    h_temp, w_temp = temp_image.shape[:2]
    ctr_x, ctr_y = w_temp // 2, h_temp // 2
    # print("temp w/h: ", w_temp, h_temp )
    matrix_rotate = cv2.getRotationMatrix2D((ctr_x,ctr_y), -angle ,1.0)
     # get cos and sin value from the rotation matrix
    cos, sin = abs(matrix_rotate[0, 0]), abs(matrix_rotate[0, 1])
    # calculate new width and height after rotation 
    newW = int((h_temp * sin) + (w_temp * cos))
    newH = int((h_temp * cos) + (w_temp * sin))
    # print("temp rotate w/h: ",newW, newH)
    # calculate new rotation center
    matrix_rotate[0, 2] += (newW / 2) - ctr_x
    matrix_rotate[1, 2] += (newH / 2) - ctr_y

    rotated_image = cv2.warpAffine(src=temp_image, M=matrix_rotate, dsize=(newW, newH))
    arr_mask = np.full((h_temp, w_temp,1),(255), dtype=np.uint8)
    mask = cv2.warpAffine(src=arr_mask, M=matrix_rotate, dsize=(newW, newH))
    # cv2.imwrite( "template_rotation.jpg",rotated_image)
    # cv2.imwrite("mask_rota.jpg",mask)

    return  rotated_image, mask, newW, newH