import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


input_pixel = [[1,1],[3,1],[5,1], [7,1], [1,3], [3,3], [5,3], [7,3]]
input_rb = [[12,1],[3,1],[5,1], [7,1], [1,3], [3,3], [5,3], [7,3]]




# /////////////////////////////////code mau

# import numpy as np
# from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt

# # Tạo dữ liệu mẫu
# np.random.seed(42)
# num_samples = 100
# xp = np.random.rand(num_samples) * 10  # Tọa độ pixel x
# yp = np.random.rand(num_samples) * 10  # Tọa độ pixel y
# x = 2 * xp + 1 + np.random.randn(num_samples)  # Tọa độ thực tế x
# y = 3 * yp - 2 + np.random.randn(num_samples)  # Tọa độ thực tế y

# # Reshape để phù hợp với yêu cầu của scikit-learn
# data = np.column_stack((xp, yp, x, y))

# # Phân chia dữ liệu thành đầu vào (xp, yp) và đầu ra (x, y)
# xpyp = data[:, :2]
# xy = data[:, 2:]

# # Tạo mô hình và huấn luyện
# model = LinearRegression()
# model.fit(xpyp, xy)

# # Dự đoán tọa độ thực từ tọa độ pixel mới
# xpyp_new = np.array([[3.5, 4.0]])  # Tọa độ pixel mới cần dự đoán
# xy_pred = model.predict(xpyp_new)
# print("Dự đoán tọa độ thực từ tọa độ pixel mới:", xy_pred[0])

# # Vẽ biểu đồ để hiển thị mô hình
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(xpyp[:, 0], xpyp[:, 1], xy[:, 0], label='Dữ liệu huấn luyện (x)')
# ax.scatter(xpyp[:, 0], xpyp[:, 1], xy[:, 1], label='Dữ liệu huấn luyện (y)')
# ax.scatter(xpyp_new[0, 0], xpyp_new[0, 1], xy_pred[0, 0], color='green', marker='x', s=100, label='Dự đoán cho tọa độ mới (x)')
# ax.scatter(xpyp_new[0, 0], xpyp_new[0, 1], xy_pred[0, 1], color='blue', marker='x', s=100, label='Dự đoán cho tọa độ mới (y)')
# ax.set_xlabel('Tọa độ pixel x')
# ax.set_ylabel('Tọa độ pixel y')
# ax.set_zlabel('Tọa độ thực tế')
# plt.legend()
# plt.show()
