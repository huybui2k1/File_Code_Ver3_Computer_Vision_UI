import cv2
import numpy as np

def rotate_template(template_gray, angle):
    (h,w) = template_gray.shape[0], template_gray.shape[1]
    cx,cy = h//2, w//2
    M = cv2.getRotationMatrix2D((cx,cy), -angle,1.0)
    cos, sin = abs(M[0, 0]), abs(M[0, 1])
    newW = int((h * sin) + (w * cos))
    newH = int((h * cos) + (w * sin))
    # calculate new rotation center
    M[0, 2] += (newW / 2) 
    M[1, 2] += (newH / 2) - cy - 10
    result = cv2.warpAffine(template_gray, M, (newW, newH), borderValue=(0, 0, 0), flags=cv2.INTER_LINEAR)
   
    pixel_array = np.full((h, w, 1), (255), dtype=np.uint8)
    mask = cv2.warpAffine(pixel_array, M, (newW, newH))
    cv2.imwrite("mask_rota.jpg",mask)
    
    return result, mask, newH, newW
    