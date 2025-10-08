# backend/utils/helpers.py
import numpy as np
import re

def parse_matrix_from_string(matrix_str):
    """
    Chuyển đổi một chuỗi có các số được phân tách bằng dấu cách hoặc dòng mới
    thành một mảng NumPy.
    """
    # Loại bỏ các ký tự không hợp lệ và chuẩn hóa dấu phân tách
    cleaned_str = re.sub(r'[;\n,]+', '\n', matrix_str).strip()
    
    # Tách chuỗi thành các hàng
    rows = cleaned_str.split('\n')
    
    # Chuyển đổi mỗi hàng thành một danh sách các số float
    matrix_list = []
    for row in rows:
        # Tách các số trong hàng, bỏ qua các khoảng trắng thừa
        elements = [float(num) for num in row.split()]
        if elements:
            matrix_list.append(elements)
    
    if not matrix_list:
        raise ValueError("Dữ liệu ma trận đầu vào rỗng.")
        
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