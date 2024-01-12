from flask import Flask, request
import numpy as np
from components import *
from ultis import *
from copy import deepcopy
from API_flask import create_app
import csv
import time
import threading
# import keyboard

logger = logging.getLogger(__name__)
app = Flask(__name__)
app = create_app()

@app.route('/cvu_process', methods=['GET','POST'])
def cvu_process():

  start_time = time.time()
# /////////Input////////////////////
  if request.method == "POST":
      #///Form data
      imgLink = request.form.get('imgLink')
      templateLink = request.form.get('templateLink')
      modelLink = request.form.get('modelLink')
      homographyLink = request.form.get('homographyLink')
      pathSaveOutputImg = request.form.get('pathSaveOutputImg')
      csvLink = request.form.get('csvLink')
      outputImgLink = request.form.get('outputImgLink')

      try:      
            min_modify = int(request.form.get('min_modify'))
            max_modify = int(request.form.get('max_modify'))
            configScore = float(request.form.get('configScore'))
            img_size = int(request.form.get('img_size'))
            method = request.form.get('method')
            similarScore = float(request.form.get('similarScore'))

      except Exception as e:
            logger.error(f'{e}\n')
            return f'{e}\n'

      #/////////Begin process/////////////////
      imgLink = imgLink.replace('\\', '/')
      templateLink = templateLink.replace('\\', '/')
      img = cv2.imread(imgLink)
      template = cv2.imread(templateLink)
      template = cv2.resize(template, (180,120))
      gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
      copy_of_template_gray = deepcopy(template_gray)
      minus_modify_angle = np.arange(0, min_modify, -1) 
      plus_modify_angle = np.arange(0, max_modify, 1) 
      low_clip, high_clip=5.0, 97.0
      copy_of_template_gray = contrast_stretching(copy_of_template_gray,  low_clip,high_clip)
      _, copy_of_template_gray = cv2.threshold(copy_of_template_gray, 100, 255, cv2.THRESH_BINARY_INV)
      intensity_of_template_gray = np.sum(copy_of_template_gray == 0)
      findCenter_type = 0
      good_points = []
      print(similarScore)
      print(method)
      print(configScore)
      try:
            len_obj,object_item = proposal_box_yolo(imgLink,modelLink,img_size,configScore)#object_item sẽ gồm list thông tin góc và tọa độ của đường bao
            print("length: ",len_obj)
            if object_item == None:
                 extractCSV(csv_file_path,result,score)
                 cv2.imwrite("Output.jpg",img)
                 return []
            for angle,bboxes,_ in object_item:
                #   print("------------------------------------------------------------")
                  result_queue = []
                  if angle == 360:
                       angle = 0
                       minus_sub_angles, plus_sub_angles = angle + minus_modify_angle, angle + plus_modify_angle
                  else:
                       minus_sub_angles, plus_sub_angles = angle + minus_modify_angle, angle + plus_modify_angle
                  # threshold = 0.95
                  point = match_pattern(gray_img, template_gray, bboxes, angle, eval(method)) 
                  if point is None:
                        continue
                  p1 = threading.Thread(target=find_center2_test, args=(gray_img,bboxes,low_clip,high_clip, intensity_of_template_gray, findCenter_type,result_queue,))
                  p2 = threading.Thread(target=compare_angle_test, args=(point,minus_sub_angles,plus_sub_angles, gray_img, template_gray, bboxes, angle, eval(method),result_queue,))
                  p1.start()
                  p2.start()   
                  p1.join()
                  p2.join()
                  bestAngle, bestPoint = result_queue[1]
                  # print("best angle: ", bestAngle)
                  center_obj, possible_grasp_ratio =  result_queue[0]
                  
                  if center_obj[0] == None and center_obj[1] == None or center_obj == None:
                        print("no center!")
                        continue       
                  if center_obj[0] < 800.0 or center_obj[0] > 2750.0:
                       print("out range!")
                       continue   
                  if center_obj[1] < 100.0 or center_obj[1] > 1950.0:
                       print("out range!")
                       continue  
                  if possible_grasp_ratio < similarScore:
                        print("score small than",similarScore)
                        continue
                  good_points.append([center_obj,bestAngle,possible_grasp_ratio])
                  # Viết chữ lên hình ảnh
                  cv2.putText(img, f"{bestAngle}", (int(center_obj[0]),int(center_obj[1] )), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                  # cv2.putText(img, f"({center_obj[0]},{center_obj[1]})", (int(center_obj[0]),int(center_obj[1] )), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
                  x2, y2 = int(center_obj[0] + 120* np.cos(np.radians(90-bestAngle)) ),int(center_obj[1]  + 120* np.sin(np.radians(90-bestAngle)) )
                  x3, y3 = int(center_obj[0] + 80* np.cos(np.radians(-bestAngle)) ),int(center_obj[1]  + 80* np.sin(np.radians(-bestAngle)) )
                  cv2.line(img,(center_obj[0],center_obj[1] ),(x2,y2),(255,0,255),2)
                  cv2.line(img,(center_obj[0],center_obj[1] ),(x3,y3),(255,255,0),2)
            print("good point arr: ",good_points)
            cv2.imwrite("Output.jpg",img)
            csv_file_path = csvLink
            # create_homography()
        
            result,score = convert_point(good_points,homographyLink)
            if len(result) != 0:     
                  extractCSV(csv_file_path,result,score)
                  result = result.tolist()
                  result.insert(0,[len_obj])
                  result.insert(0,[len(good_points)])
            print("result: ", result)
            print("time process: ",time.time() - start_time)
            return result
            # return []

      except Exception as e:
           csv_file_path = csvLink
           result = [[0,0,0,0]]
           score = []
           extractCSV(csv_file_path,result,score)
           cv2.imwrite("Output.jpg",img)
           print("System error: ", e)
           return []

@app.route('/get_total', methods=['GET','POST'])
def get_total():

  start_time = time.time()
# /////////Input////////////////////
  if request.method == "POST":
      try:      
            #///Form data
            configScore = float(request.form.get('configScore'))
            img_size = int(request.form.get('img_size'))
            imgLink = request.form.get('imgLink')
            modelLink = request.form.get('modelLink')
      except Exception as e:
            logger.error(f'{e}\n')
            return f'{e}\n'

      #/////////Begin process/////////////////
      imgLink = imgLink.replace('\\', '/')     
      try:
            len_obj,object_item = proposal_box_yolo(imgLink,modelLink,img_size,configScore)#object_item sẽ gồm list thông tin góc và tọa độ của đường bao
            img = cv2.imread(imgLink)
            cv2.imwrite("Output.jpg",img)
            print("length: ",len_obj)
            result = []
            result.append(len_obj)
            print("time process: ",time.time() - start_time)
            return [result]
            # return []

      except Exception as e:
           print("System error: ", e)
           return []
      print(configScore)
      print(imgLink)
      print(img_size) 

if __name__ == "__main__":
     app.run()