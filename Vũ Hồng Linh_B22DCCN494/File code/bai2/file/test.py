import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Dữ liệu giả lập
X = np.array([[1], [2], [3], [4], [5]])  # Biến độc lập
y = np.array([1, 2, 3, 3.5, 5])         # Biến phụ thuộc

# Khởi tạo mô hình hồi quy tuyến tính
model = LinearRegression()

# Huấn luyện mô hình
model.fit(X, y)

# Dự đoán
y_pred = model.predict(X)

# Vẽ biểu đồ hồi quy
plt.scatter(X, y, color='blue', label='Dữ liệu thực')
plt.plot(X, y_pred, color='red', label='Dự đoán hồi quy')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()

# Hiển thị các trọng số
print(f"Hệ số w_1: {model.coef_}")
print(f"Hệ số tự do w_0: {model.intercept_}")
