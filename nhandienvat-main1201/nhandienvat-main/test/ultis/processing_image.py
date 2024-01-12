import cv2
import numpy as np


def contrast_stretching(img, low_clip=2.0, high_clip=97.0):
    if img.size == 0:
        return img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    low_val, high_val = np.percentile(img, (low_clip, high_clip))
    out_img = np.uint8(np.clip((img - low_val) * 255.0 / (high_val - low_val), 0, 255))
    return out_img

# /////////////Khái niêm 

# Phân vị (percentiles) thường được sử dụng trong kỹ thuật xử lý ảnh gọi là "contrast stretching" (mở rộng độ tương phản). Contrast stretching giúp cải thiện độ tương phản của ảnh bằng cách làm cho các giá trị pixel trong ảnh mở rộng từ một khoảng giá trị nhất định.

# Trong contrast stretching, phân vị được sử dụng để xác định giới hạn của khoảng giá trị pixel mới sau khi áp dụng phép biến đổi. Phép biến đổi này giúp đưa các giá trị pixel gần phân vị thấp về 0 và giá trị pixel gần phân vị cao về 255 (đối với ảnh 8-bit).