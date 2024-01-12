import cv2

def shrink_image(output_image_path, scale_percent):
    # Đọc hình ảnh từ đường dẫn
    img = cv2.imread(r"C:\Users\TKD01A-1\Documents\PHAMCAOTHANG_DOC\nhandienvat-main\nhandienvat-main\test\test_homography\drive-download-20231220T065754Z-001\20231220_135604.jpg")

    # Lấy kích thước hiện tại của hình ảnh
    width = int(img.shape[1])
    height = int(img.shape[0])

    # Tính toán tỉ lệ mới dựa trên percent được đưa vào
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)

    # Thực hiện thay đổi tỉ lệ hình ảnh
    resized_img = cv2.resize(img, (new_width, new_height))

    # Ghi hình ảnh đã thay đổi vào đường dẫn đầu ra
    cv2.imwrite(output_image_path, resized_img)



# Đường dẫn đến hình ảnh đầu ra (thay đổi theo ý muốn)
output_path = 'C:/Users/TKD01A-1/Documents/PHAMCAOTHANG_DOC/nhandienvat-main/nhandienvat-main/test/test_homography/resized_image2.jpg'

# Tỉ lệ thu nhỏ (ở đây là 50%, bạn có thể thay đổi theo ý muốn)
scale_percent = 30

# Gọi hàm để thu nhỏ hình ảnh và lưu kết quả
shrink_image(output_path, scale_percent)