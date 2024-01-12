import cv2
from ultis.rotate_object import rotate_object 
import logging


logger = logging.getLogger(__name__)
# mở rộng khung ảnh một khi tọa độ bbox ở sát khung ảnh, cản trở việc roi đối tượng
def padded_image(img_gray, bboxes, esilon_w,epsilon_h):
   x_start,y_start  = bboxes[0] - esilon_w, bboxes[1] - epsilon_h
   x_end, y_end = bboxes[0] + bboxes[2] + esilon_w, bboxes[1] + bboxes[3] + epsilon_h
   padded_left, padded_top = min(x_start,0), min(y_start,0)
   padded_right, padded_bottom = min(img_gray.shape[1] - x_end, 0), min(img_gray.shape[0] - y_end,0)
   
   # print("paded: ",padded_left, padded_top, padded_right, padded_bottom)
   img_padded = cv2.copyMakeBorder(img_gray,abs(padded_top),abs(padded_bottom), abs(padded_left), abs(padded_right),cv2.BORDER_CONSTANT, value=0 )

   return img_padded, x_start, x_end, y_start, y_end


def match_pattern(img_gray, template_gray, boxes, sub_angle, method ):
   try:

      rotated_template,mask, w_temp,h_temp = rotate_object(template_gray,sub_angle)
      epsilon_w, epsilon_h = abs(boxes[2]-w_temp), abs(boxes[3]-h_temp)
      # print("epsilon_w, epsilon_h", epsilon_w, epsilon_h,boxes[2],boxes[3])
      img_padded, x_start, x_end, y_start, y_end = padded_image(img_gray,boxes, epsilon_w, epsilon_h)
      img_roi = img_padded[abs(y_start) : abs(y_end)  ,abs(x_start) : abs(x_end)]
      check = img_roi.size - rotated_template.size 
      
      cv2.imwrite("img_roi_match.jpg",img_roi)
      cv2.imwrite("rotated_template_match.jpg",rotated_template)
      matched_points = cv2.matchTemplate(img_roi, rotated_template, method, None, mask)
      _, max_val, _, _ = cv2.minMaxLoc(matched_points)
      # print("point mark: ", max_val)

      return max_val
   
   except Exception as a:
      print("error of match: ",a)
      return 0



# matched_points là một mảng hai chiều chứa các điểm tương tự hoặc giá trị liên quan đến mức độ khớp giữa mẫu và ảnh. Mỗi phần tử trong mảng tương ứng với mức độ khớp tại một vị trí cụ thể trong ảnh.

# Hàm cv2.minMaxLoc được sử dụng để tìm giá trị nhỏ nhất và lớn nhất trong mảng matched_points và cũng trả về vị trí (tọa độ x, y) của giá trị lớn nhất.

# Khi bạn gán kết quả từ cv2.minMaxLoc cho các biến _, max_val, _, và max_loc, bạn có các giá trị sau:

# _ (underscore đầu tiên) là giá trị nhỏ nhất trong mảng matched_points, nhưng bạn không sử dụng nó trong ví dụ này, vì bạn chỉ quan tâm đến giá trị lớn nhất.
# max_val là giá trị lớn nhất trong mảng matched_points. Đây có thể được coi là mức độ khớp tối đa giữa mẫu và vùng quan tâm của ảnh.
# _ (underscore thứ hai) là vị trí (tọa độ x, y) của giá trị nhỏ nhất trong mảng, bạn cũng không sử dụng nó.
# max_loc là vị trí (tọa độ x, y) của giá trị lớn nhất trong mảng matched_points. Nó cho biết vị trí tương ứng trên ảnh gốc (img_gray) mà mẫu có mức độ khớp tối đa.
# Sau dòng mã này, bạn có thể sử dụng giá trị max_val để xem mức độ khớp tối đa và max_loc để biết vị trí tương ứng trên ảnh.