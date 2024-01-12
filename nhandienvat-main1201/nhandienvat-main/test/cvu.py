from flask import Flask, request
import numpy as np
from components import *
from ultis import *
from copy import deepcopy
from API_flask import create_app
import csv
import time
import multiprocessing as mp
# import keyboard

logger = logging.getLogger(__name__)

app = create_app()


@app.route('/cvu_process', methods=['GET','POST'])
def cvu_process():
#   model = YOLO('yolov8n-seg.pt')  # load an official model
#   model = YOLO(r'C:\Users\TKD01A-1\Documents\PHAMCAOTHANG_DOC\nhandienvat-main\nhandienvat-main\test\runs\segment\train\weights\last.pt')  # load a custom model
  start_time = time.time()
# /////////Input////////////////////
  if request.method == "POST":
      #///Form data
      imgLink = request.form.get('imgLink')
      templateLink = request.form.get('templateLink')
      modelLink = request.form.get('modelLink')
      pathSaveOutputImg = request.form.get('pathSaveOutputImg')

      try:
            csvLink = request.form.get('csvLink')
            outputImgLink = request.form.get('outputImgLink')
            min_modify = int(request.form.get('min_modify'))
            max_modify = int(request.form.get('max_modify'))
            configScore = float(request.form.get('configScore'))
            img_size = int(request.form.get('img_size'))
            method = request.form.get('method')
            server_ip = request.form.get('server_ip')

      except Exception as e:
            logger.error(f'{e}\n')
            return f'{e}\n'

      #/////////Begin process/////////////////
      imgLink = imgLink.replace('\\', '/')
      templateLink = templateLink.replace('\\', '/')
      img = cv2.imread(imgLink)
      template = cv2.imread(templateLink)
      resize_w,resize_h = 255,165
      template = cv2.resize(template, (resize_w,resize_h))
      gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
      copy_of_template_gray = deepcopy(template_gray)
      minus_modify_angle = np.arange(0, min_modify, -2) #-20
      plus_modify_angle = np.arange(0, max_modify, 2) #20
      low_clip=5.0
      high_clip=97.0
      copy_of_template_gray = contrast_stretching(copy_of_template_gray,  low_clip,high_clip)
      _, copy_of_template_gray = cv2.threshold(copy_of_template_gray, 100, 255, cv2.THRESH_BINARY_INV)
      # cv2.imwrite("thresTemp.jpg",copy_of_template_gray)
      intensity_of_template_gray = np.sum(copy_of_template_gray == 0)
      findCenter_type = 0
      good_points = []
      try:
            # print("Run API...")
            object_item = proposal_box_yolo(imgLink,modelLink,img_size,configScore)#object_item sẽ gồm list thông tin góc và tọa độ của đường bao
            # print("in4: ", object_item)
            if object_item == None:
                 return good_points
            #Result array
            
            for angle,bboxes,class_ids in object_item:
                  # result_queue = mp.Queue()
                  # p1 = mp.Process(target=find_center2, args=(gray_img,bboxes,low_clip,high_clip, intensity_of_template_gray, findCenter_type,result_queue))
                  # p1.start()
                  # p1.join()
                  # result = []
                  # while not result_queue.empty():
                  #       result.append(result_queue.get())
                  # print("result: ",result)
                  # print("result one by one: ",result[0][0])
                  # center_0,center_1, possible_grasp_ratio =  result[0]
                  # center_obj = (center_0,center_1)
                  # print("center_obj, possible_grasp_ratio",center_obj[0],center_obj[1], possible_grasp_ratio)
                  #    p2 = mp.Process(target=print_cube, args=(10, ))
                  #///////////////////////////////////////////////////////////////////
                  center_obj, possible_grasp_ratio  = find_center2(gray_img,bboxes,low_clip,high_clip, intensity_of_template_gray, findCenter_type)     
                  # if angle <= 0:
                  #      angle = 360 + angle
                  if center_obj[0] == None and center_obj[1] == None:
                       continue          
                  if possible_grasp_ratio < 90:
                        print("score<95!")
                        continue
                  
                  # cv2.circle(img,(int(center_obj[0]),int(center_obj[1])),2,(0, 0, 255) ,-1)
                  minus_sub_angles = angle + minus_modify_angle
                  plus_sub_angles = angle + plus_modify_angle
                  
                  # threshold = 0.95
                  point = match_pattern(gray_img, template_gray, bboxes, angle, eval(method)) 
                  
                  if point is None:
                        continue
                  bestAngle, _ = compare_angle(point,minus_sub_angles,plus_sub_angles, gray_img, template_gray, bboxes, angle, eval(method))

                  # Viết chữ lên hình ảnh
                  cv2.putText(img, f"{bestAngle}", (int(center_obj[0]),int(center_obj[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                  x2, y2 = int(center_obj[0] + 150* np.cos(np.radians(bestAngle)) ),int(center_obj[1] + 150* np.sin(np.radians(bestAngle)) )
                  x3, y3 = int(center_obj[0] + 100* np.cos(np.radians(bestAngle+90)) ),int(center_obj[1] + 100* np.sin(np.radians(bestAngle+90)) )
                  cv2.line(img,center_obj,(x2,y2),(255,255,0),2)
                  cv2.line(img,center_obj,(x3,y3),(255,0,255),2)
                  cv2.imwrite("amTam.jpg",img)
                  # print("total: ",center_obj[0],center_obj[1],bestAngle,possible_grasp_ratio)


                  result = [center_obj[0],center_obj[1],bestAngle,possible_grasp_ratio]
                  good_points.append(result)
                  # print("Chờ đợi nhấn phím...")

                  # keyboard.wait("enter")  # Chờ đợi đến khi phím Enter được nhấn

                  # print("Phím Enter đã được nhấn. Tiếp tục thực thi code.")
            # resize(imgLink,pathSaveOutputImg)
            # print("good point arr: ",good_points)

            end_time = time.time()
            a = end_time - start_time
            print("process time: ",a)
            return f'{good_points}'
      except Exception as e:
           print("System error: ",e)
           return good_points

#   if request.method == "GET":
#        return f'<div><h1>Get result</h1></div>'
       

if __name__ == "__main__":
     app.run(debug=True)