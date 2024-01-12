import cv2
import numpy as np
from ultis.processing_image import contrast_stretching



def find_center(gray_img,bboxes, low_clip,high_clip,intensity_of_template_gray,findCenter_type,result_queue):

    # print("time excute: ", time.time())
    x1,y1,w,h = bboxes[0]-5, bboxes[1]-5, bboxes[2], bboxes[3]
    # c1,c2 = x1 + w/2, y1 + h/2
    center_obj = (0,0)
    if(x1<10 or y1 <10):
     gray_img = cv2.copyMakeBorder(gray_img,20,20, 20, 20,cv2.BORDER_CONSTANT, value=0 )
    imgRoi = gray_img[y1 :y1+h ,x1 :x1+w ]
    
    padded_roi_gray = gray_img[y1-15:y1+h + 15,x1-15:x1+w + 15]
   
    thresholdImg = contrast_stretching(imgRoi,low_clip,high_clip)
    padded_thresholdImg = contrast_stretching(padded_roi_gray,  low_clip,high_clip)
    _,thresholdImg = cv2.threshold(thresholdImg,100,255, cv2.THRESH_BINARY_INV)
    _,padded_roi_gray = cv2.threshold(padded_thresholdImg,100,255, cv2.THRESH_BINARY_INV)
    intensity_of_roi_gray = np.sum(padded_roi_gray == 0)
    # print("temp-padded: ",intensity_of_template_gray,intensity_of_roi_gray)
    if intensity_of_roi_gray != 0:
        possible_grasp_ratio = (intensity_of_template_gray / intensity_of_roi_gray) * 100
        print("score: ",possible_grasp_ratio)
    else:
        possible_grasp_ratio = 0
    if findCenter_type == 0:
        try:
            contours,_ = cv2.findContours(thresholdImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            check_true = False
            for element in contours:
                s = cv2.contourArea(element)             
               
                if s < 1080 or s > 1165:
                    continue
                # print('S contour: ',s)
                check_true = True
                (x_axis, y_axis), radius = cv2.minEnclosingCircle(element)
                center = (int(x_axis + x1 ),int(y_axis + y1 )) 
                radius = int(radius) 
                cv2.circle(gray_img,center,radius,(0,255,0),1) 
                cv2.circle(gray_img,center,1,(255,255,0),3) 
                # cv2.imwrite("img_paded2.jpg",gray_img)
                center_obj = (center[0],center[1])
                break
            if check_true == False:
                center_obj = (None, None)

        except Exception as e:
                center_obj = (None, None)
    result_queue.append((center_obj,possible_grasp_ratio))
    return center_obj, possible_grasp_ratio


def find_center2_test(gray_img,bboxes, low_clip,high_clip,intensity_of_template_gray,findCenter_type,result_queue):

    # print("time excute: ", time.time())
    x1,y1,w,h = bboxes[0], bboxes[1], bboxes[2], bboxes[3]
    # c1,c2 = x1 + w/2, y1 + h/2
    center_obj = (0,0)
    if(x1<10 or y1 <10):
     gray_img = cv2.copyMakeBorder(gray_img,20,20, 20, 20,cv2.BORDER_CONSTANT, value=0 )
    imgRoi = gray_img[y1 :y1+h ,x1 :x1+w ]
    
    ret,thresh = cv2.threshold(imgRoi,127,255,0)
    M = cv2.moments(thresh)
    # Kiểm tra xem M["m00"] có khác 0 hay không trước khi thực hiện phép chia
 

    padded_roi_gray = gray_img[y1-15:y1+h + 15,x1-15:x1+w + 15]
    thresholdImg = contrast_stretching(imgRoi,low_clip,high_clip)
    padded_thresholdImg = contrast_stretching(padded_roi_gray,  low_clip,high_clip)
    _,thresholdImg = cv2.threshold(thresholdImg,100,255, cv2.THRESH_BINARY_INV)
    _,padded_roi_gray = cv2.threshold(padded_thresholdImg,100,255, cv2.THRESH_BINARY_INV)
    
  
    intensity_of_roi_gray = np.sum(padded_roi_gray == 0)
    # print("temp-padded: ",intensity_of_template_gray,intensity_of_roi_gray)
    if intensity_of_roi_gray != 0:
        possible_grasp_ratio = (intensity_of_template_gray / intensity_of_roi_gray) * 100
        # print("sosanh: ",possible_grasp_ratio)
    else:
        possible_grasp_ratio = 0
    if findCenter_type == 0:
        try:
            contours,_ = cv2.findContours(thresholdImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            check_true = False
            for element in contours:
                s = cv2.contourArea(element)
                if s < 1000 or s > 1350:
                    continue
                # print('S contour: ',s)
                check_true = True
                (x_axis, y_axis), radius = cv2.minEnclosingCircle(element)
                center = (int(x_axis + x1 ),int(y_axis + y1 )) 
                radius = int(radius) 
                # cv2.circle(gray_img,center,radius,(0,255,0),1) 
                # cv2.circle(gray_img,center,1,(255,255,0),3) 
                # cv2.circle(gray_img, (cx, cy), 5, (255, 255, 255), -1)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M['m01'] / M["m00"])
                    cx, cy = cX + x1, cY + y1
                    compareX,compareY = abs(center[0]-cx), abs(center[1]-cy)
                    print("sdsad: ",compareX,compareY )
                    if compareX < 20 and compareY < 20:
                        center_obj = (center[0],center[1])
                else:
                    center_obj = (center[0],center[1])
            if check_true == False:
                center_obj = (None, None)

        except Exception as e:
                center_obj = (None, None)
    result_queue.append((center_obj,possible_grasp_ratio))
    return center_obj, possible_grasp_ratio