import cv2
import numpy as np

img_src = cv2.imread(r"C:\Users\TKD01A-1\Documents\PHAMCAOTHANG_DOC\nhandienvat-main\nhandienvat-main\test\test_homography\resized_image1.jpg")
img_predict = cv2.imread(r"C:\Users\TKD01A-1\Documents\PHAMCAOTHANG_DOC\nhandienvat-main\nhandienvat-main\test\test_homography\resized_image2.jpg")

point_src = []
point_predict = []
cv2.imshow("img_src_windows",img_src)
def click_write_point(event, x, y, flags, param):
    global img_src, point_src

    if event == cv2.EVENT_LBUTTONDOWN:
        point_src.append((x, y))
        cv2.circle(img_src, (x, y), radius=2, color=(255, 255, 0), thickness=-1)
        text = f"({x}, {y})"
        cv2.putText(img_src, text, (x + 2, y + 2), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 255), thickness=1)
        cv2.imshow("img_src_windows",img_src)

cv2.setMouseCallback('img_src_windows', click_write_point)
cv2.waitKey(0)

cv2.imshow("img_predict_windows",img_predict)
def click_write_point2(event, x, y, flags, param):
    global img_predict, point_predict

    if event == cv2.EVENT_LBUTTONDOWN:
        point_predict.append((x, y))
        cv2.circle(img_predict, (x, y), radius=2, color=(255, 255, 0), thickness=-1)
        text = f"({x}, {y})"
        cv2.putText(img_predict, text, (x + 2, y + 2), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 255), thickness=1)
        cv2.imshow("img_predict_windows",img_predict)

cv2.setMouseCallback('img_predict_windows', click_write_point2)
cv2.waitKey(0)

point_src = np.array(point_src)
point_predict = np.array(point_predict)

# Tính toán ma trận homography
H, _ = cv2.findHomography(point_src, point_predict)
print("homography matrix: ", H)
output_file_path = 'homography_matrix_img.npy'
np.save(output_file_path, H)
# Chuyển tọa độ của một điểm từ hình ảnh gốc sang hình ảnh đích
point_to_transform = np.array([[468,111,1],[235,325,1],[103,429,1],[370,376,1]], dtype=float).T
# print("jlkjlk: ",point_to_transform)
matrix = np.load(r'C:\Users\TKD01A-1\Documents\PHAMCAOTHANG_DOC\nhandienvat-main\nhandienvat-main\test\test_homography\homography_matrix_img.npy')
transformed_point = np.dot(matrix, point_to_transform)

# Chia cho phần tử cuối cùng để có tọa độ (x, y, 1)
transformed_point /= transformed_point[2]
# print(np.array([[1919, 1851,1], [1894, 1574,1], [2165, 1822,1], [1449, 1869,1]],dtype=float))
print("return: ",transformed_point)
for point in transformed_point[:2].T:
    cv2.circle(img_predict, (int(point[0]), int(point[1])), radius=3, color=(0, 255, 255), thickness=-1)

cv2.imwrite("out.jpg",img_predict)
output_file_path = 'homography_matrix.npy'
np.save(output_file_path, H)
print("Tọa độ của điểm sau khi chuyển đổi:")
print(transformed_point[:2].T)

print("point: ",point_src)
print("point predict: ",point_predict)

cv2.destroyAllWindows()