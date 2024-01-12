import numpy as np
import cv2


def create_homography():
    input_pixel = np.array([[665, 707], [644, 1329], [1318, 1687], [1916, 1632 ],  [2199, 1057],[2083, 420], [1463, 257]],dtype=float)
    input_rb = np.array([[341,-46],[423,-45],[471,43],[462,123],[386,158],[302,142],[282,60]],dtype=float)
    print("input_pixel: ", input_pixel)
    print("input_rb: ", input_rb)
    #toa do tung vi tri theo toa do cua robot
    # Ước lượng ma trận homography bằng RANSAC
    homography_matrix, _ = cv2.findHomography(input_pixel, input_rb, cv2.RANSAC, 5.0)
    output_file_path = 'homography_matrix.npy'
    np.save(output_file_path, homography_matrix)
    # In ma trận homography
    print("Homography Matrix:")
    print(homography_matrix)

def convert_point(point,input_file_path):
    try:
        center = np.array([sublist[0] for sublist in point],dtype=np.float32)
        angle = np.array([sublist[1] for sublist in point],dtype=np.float32)
        score = np.array([sublist[2] for sublist in point],dtype=np.float32)
        center = np.hstack((center, np.ones((center.shape[0], 1)))).T
        # # Nạp ma trận homography từ tệp tin .npy
        homography_matrix = np.load(input_file_path)
        # print("matrix: ",homography_matrix)
        transformed_point = np.dot(homography_matrix, center)
        # Chia cho phần tử cuối cùng để có tọa độ (x, y, 1)
        transformed_point = transformed_point / transformed_point[2]
        center_point = transformed_point[:2].T
        # print("result convert: ",center_point)
        result = np.array(list(zip(center_point[:,0],center_point[:,1], angle)), dtype=np.float32)
        # return transformed_point[0], transformed_point[1]
        return result,score
    except Exception as e:
        # print("System error: ", e)
        return [],[]
    
