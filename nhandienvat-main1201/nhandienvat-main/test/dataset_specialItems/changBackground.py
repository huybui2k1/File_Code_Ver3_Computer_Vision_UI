
import cv2
import numpy as np

# Đọc ảnh ban đầu
image =  cv2.imread(r"E:\My_Code\NhanDienvat\detectByYolov8\dataset_specialItems\train\images\20230922_154821_jpg.rf.a42c5a9c92cd44eab2b221cae3f1cd31.jpg")



# # Áp dụng bộ lọc Gaussian
# ksize = (5, 5)  # Kích thước của kernel (cỡ của vùng làm mịn)
# sigma = 0       # Độ lớn của Gaussian kernel

# # Sử dụng hàm cv2.GaussianBlur để làm mịn ảnh
# smoothed_image = cv2.GaussianBlur(image, ksize, sigma)



# # Kích thước kernel cho bộ lọc Average (chọn kích thước lớn hơn để làm mờ mạnh hơn)
# kernel_size = (3, 3)

# # Sử dụng hàm cv2.blur để làm mờ ảnh với bộ lọc trung bình
# blurred_image = cv2.blur(smoothed_image, kernel_size)

# # Tăng cường độ tương phản (có thể điều chỉnh giá trị alpha để tăng hoặc giảm độ tương phản)
# alpha = -2.0  # Tăng độ tương phản

# # Sử dụng hàm cv2.convertScaleAbs để tăng cường độ tương phản
# enhanced_image = cv2.convertScaleAbs(image, alpha=alpha, beta=0)


# Giảm độ sáng của ảnh (có thể điều chỉnh giá trị beta để giảm hoặc tăng độ sáng)
beta = -50  # Giảm độ sáng

# Sử dụng hàm cv2.convertScaleAbs để giảm độ sáng của ảnh
darkened_image = cv2.convertScaleAbs(image, alpha=1, beta=beta)

# # Hiển thị ảnh gốc và ảnh đã làm mịn
# cv2.imwrite("SmoothedImage.jpg",smoothed_image)
# cv2.imshow('Original Image', image)
# cv2.imshow('Smoothed Image', smoothed_image)



# # Hiển thị ảnh gốc và ảnh đã làm mờ
# cv2.imshow('Original Image', image)
# cv2.imshow('Blurred Image', blurred_image)

cv2.imwrite("darkened_image.jpg",darkened_image)
# # Hiển thị ảnh gốc và ảnh đã tăng cường độ tương phản
# cv2.imshow('Original Image', image)
# cv2.imshow('Enhanced Image', enhanced_image)


# Hiển thị ảnh gốc và ảnh đã giảm độ sáng
cv2.imshow('Original Image', image)
cv2.imshow('Darkened Image', darkened_image)


# Đợi bất kỳ phím nào được nhấn và sau đó đóng cửa sổ hiển thị
cv2.waitKey(0)
cv2.destroyAllWindows()


# # Tọa độ của 4 điểm cần giữ nguyên
# points = [(25, 56), (58, 32), (125, 43), (216, 85)]

# # Tạo mask để xác định vùng cần giữ nguyên
# mask = np.zeros_like(image)

# # Vẽ đa giác trắng trên mask dựa trên các điểm
# cv2.fillPoly(mask, [np.array(points)], (255, 255, 255))

# # Xác định màu nền mới (ví dụ: màu xanh lam)
# new_background_color = (0, 0, 255)  # Màu xanh lam

# # Tạo một ảnh mới với màu nền mới
# new_background = np.full_like(image, new_background_color)

# # Kết hợp ảnh mới và ảnh ban đầu bằng mask
# result = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
# background = cv2.bitwise_and(new_background, new_background, mask=mask)
# final_image = cv2.add(result, background)

# # Lưu trữ ảnh kết quả
# cv2.imwrite('changed_background_image.jpg', final_image)

# # Hiển thị ảnh kết quả
# cv2.imshow('Changed Background Image', final_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()