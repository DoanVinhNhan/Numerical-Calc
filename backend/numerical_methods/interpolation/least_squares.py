# backend/numerical_methods/interpolation/least_squares.py
import numpy as np
from typing import List, Dict, Any
from sympy import symbols, sympify, lambdify, SympifyError
from backend.utils.helpers import zero_small

def least_squares_approximation(
    x_nodes: List[float], 
    y_nodes: List[float], 
    basis_func_strings: List[str]
) -> Dict[str, Any]:
    """
    Tìm hàm xấp xỉ g(x) bằng phương pháp bình phương tối thiểu.

    Bài toán: Cho bộ điểm (x_i, y_i) và hệ hàm cơ sở {phi_j(x)}.
    Mục tiêu: Tìm g(x) = sum(a_j * phi_j(x)) sao cho
    S = sum( (g(x_i) - y_i)^2 ) đạt giá trị nhỏ nhất.

    Thuật toán:
    1. Xây dựng ma trận Phi (n x m) với Phi[i, j] = phi_j(x_i).
    2. Xây dựng ma trận M = Phi^T * Phi (m x m).
    3. Xây dựng vector vế phải b = Phi^T * y (m x 1).
    4. Giải hệ phương trình tuyến tính M * a = b để tìm vector hệ số a.

    Parameters:
        x_nodes (List[float]): Danh sách các mốc x_i.
        y_nodes (List[float]): Danh sách các giá trị y_i tương ứng.
        basis_func_strings (List[str]): Danh sách các chuỗi biểu diễn hàm cơ sở
                                        (ví dụ: ['1', 'x', 'x**2']).

    Returns:
        Dict[str, Any]: Một từ điển chứa các hệ số, hàm kết quả, và các ma trận trung gian.
    """
    x_data = np.array(x_nodes, dtype=float)
    y_data = np.array(y_nodes, dtype=float).reshape(-1, 1)  # (n x 1)
    
    n = len(x_data)
    m = len(basis_func_strings)

    if n != len(y_data):
        raise ValueError("Số lượng mốc x và giá trị y phải bằng nhau.")
    if m == 0:
        raise ValueError("Danh sách hàm cơ sở không được rỗng.")
    if n < m:
        raise ValueError(f"Số lượng điểm dữ liệu ({n}) phải lớn hơn hoặc bằng số lượng hàm cơ sở ({m}).")

    # 1. Phân tích các hàm cơ sở từ chuỗi
    x = symbols('x')
    basis_funcs = []
    for j, func_str in enumerate(basis_func_strings):
        try:
            expr = sympify(func_str)
            basis_funcs.append(lambdify(x, expr, 'numpy'))
        except (SympifyError, TypeError) as e:
            raise ValueError(f"Hàm cơ sở '{func_str}' (hàm số {j+1}) không hợp lệ: {e}")

    # 2. Xây dựng ma trận Phi (n x m)
    phi_matrix = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            phi_matrix[i, j] = basis_funcs[j](x_data[i])
            
    # 3. Lập hệ phương trình chuẩn M * a = b
    # M = Phi^T * Phi (m x m)
    m_matrix = phi_matrix.T @ phi_matrix
    
    # b = Phi^T * y (m x 1)
    rhs_vector = phi_matrix.T @ y_data

    # 4. Giải hệ
    try:
        coefficients_vec = np.linalg.solve(m_matrix, rhs_vector)
    except np.linalg.LinAlgError:
        raise ValueError("Ma trận M = Phi^T * Phi suy biến. Không thể tìm nghiệm duy nhất. Các hàm cơ sở có thể phụ thuộc tuyến tính.")
    
    coefficients = coefficients_vec.flatten()  # Chuyển về mảng 1D

    # 5. Tính toán sai số
    y_predicted = phi_matrix @ coefficients_vec
    errors = y_data - y_predicted
    sum_squared_errors = np.sum(errors**2)
    std_error = np.sqrt(sum_squared_errors / n)

    # 6. Tạo chuỗi hàm kết quả
    g_x_str = " + ".join([f"({coeff:g}) \\cdot ({func_str})" 
                          for coeff, func_str in zip(coefficients, basis_func_strings)])
    g_x_str = g_x_str.replace("+ -", "- ") # Dọn dẹp chuỗi

    return {
        "status": "success",
        "method_name": "Bình phương tối thiểu",
        "coefficients": zero_small(coefficients).tolist(),
        "g_x_str_latex": g_x_str,
        "error_metrics": {
            "sum_squared_errors": float(sum_squared_errors),
            "std_error": float(std_error) # Sai số trung bình phương
        },
        "intermediate_matrices": {
            "phi_matrix": zero_small(phi_matrix).tolist(),
            "m_matrix": zero_small(m_matrix).tolist(),
            "rhs_vector": zero_small(rhs_vector).tolist()
        },
        "x_nodes": x_data.tolist(),
        "y_nodes": y_data.flatten().tolist()
    }