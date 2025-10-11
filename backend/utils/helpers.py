# backend/utils/helpers.py
import numpy as np
import re

def parse_matrix_from_string(matrix_str):
    """
    Chuyển đổi một chuỗi ma trận thành một mảng NumPy.
    Ném ra lỗi ValueError với thông báo tường minh nếu định dạng sai.
    """
    if not matrix_str.strip():
        raise ValueError("Lỗi: Dữ liệu đầu vào bị rỗng.")

    # Tách chuỗi thành các hàng
    rows = matrix_str.strip().split('\n')
    matrix_list = []
    num_cols = -1

    for i, row_str in enumerate(rows):
        try:
            # Tách các phần tử trong hàng và chuyển đổi sang float
            row_list = [float(num) for num in row_str.split()]
        except ValueError:
            # Nếu có lỗi, nghĩa là có ký tự không phải số
            raise ValueError(f"Lỗi định dạng ở hàng {i + 1}: Chứa ký tự không phải là số.")

        # Kiểm tra tính nhất quán của số cột
        if i == 0:
            num_cols = len(row_list)
        elif len(row_list) != num_cols:
            raise ValueError(f"Lỗi định dạng ở hàng {i + 1}: Số lượng cột không đồng nhất (hàng 1 có {num_cols} cột, hàng này có {len(row_list)} cột).")
        
        if row_list: # Chỉ thêm nếu hàng không rỗng
            matrix_list.append(row_list)
    
    if not matrix_list:
        raise ValueError("Lỗi: Dữ liệu đầu vào không chứa số nào.")
        
    return np.array(matrix_list)

def zero_small(x, tol=1e-15):
    """
    Làm tròn các giá trị rất nhỏ trong một mảng NumPy về 0.
    
    Args:
        x (np.ndarray or list): Mảng đầu vào.
        tol (float): Ngưỡng để coi một số là zero.

    Returns:
        np.ndarray: Mảng mới với các giá trị nhỏ đã được làm tròn về 0.
    """
    x_arr = np.array(x)
    x_arr[np.abs(x_arr) < tol] = 0.0
    return x_arr

def get_char_polynomial(A):
    """
    Lấy đa thức đặc trưng từ ma trận Frobenius (dạng đồng hành).
    """
    n = A.shape[0]
    p = np.zeros(n + 1, dtype=float)
    p[0] = 1.0
    if n > 0:
        p[1:] = -A[0, :].real
    return p