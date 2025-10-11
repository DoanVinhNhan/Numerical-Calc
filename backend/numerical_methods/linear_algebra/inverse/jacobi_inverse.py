# backend/numerical_methods/linear_algebra/inverse/jacobi_inverse.py
import numpy as np
from backend.utils.helpers import zero_small
from backend.numerical_methods.linear_algebra.iterative.jacobi import jacobi # Tái sử dụng hàm jacobi đã có

def jacobi_inverse(A, x0_method='method1', tol=1e-5, max_iter=100):
    """
    Tìm ma trận nghịch đảo A⁻¹ bằng cách giải hệ AX = I sử dụng phương pháp lặp Jacobi đã có.
    """
    n = A.shape[0]
    if n != A.shape[1]:
        raise ValueError("Ma trận phải là ma trận vuông.")

    # 1. Chuẩn bị ma trận ban đầu X₀ theo phương thức đã chọn
    if x0_method == 'method1':
        # X₀ = Aᵀ / ||A||₂²
        norm_val = np.linalg.norm(A, 2)
        if np.isclose(norm_val, 0):
            raise ValueError("Chuẩn 2 của ma trận A bằng 0, không thể chọn X₀.")
        X0 = A.T / (norm_val ** 2)
    elif x0_method == 'method2':
        # X₀ = Aᵀ / (||A||₁ * ||A||∞)
        norm_val = np.linalg.norm(A, 1) * np.linalg.norm(A, np.inf)
        if np.isclose(norm_val, 0):
            raise ValueError("Tích chuẩn 1 và chuẩn vô cùng của A bằng 0, không thể chọn X₀.")
        X0 = A.T / norm_val
    else:
        raise ValueError("Phương thức chọn X₀ không hợp lệ. Chỉ hỗ trợ 'method1' và 'method2'.")

    # 2. Thiết lập vế phải là ma trận đơn vị I
    I = np.eye(n)

    # 3. Gọi hàm jacobi gốc để giải hệ AX = I
    # Hàm jacobi đã xử lý đúng điều kiện chéo trội và công thức sai số hậu nghiệm
    result = jacobi(A, I, X0, tol, max_iter)
    
    # 4. Xử lý kết quả trả về
    inverse_A = result["solution"]
    check_matrix = A @ inverse_A

    # Thêm các thông tin đặc thù của bài toán nghịch đảo vào kết quả
    result["inverse"] = inverse_A
    result["check_matrix"] = check_matrix
    result["x0_method"] = x0_method
    result["initial_matrix"] = X0
    
    # Xóa các trường không cần thiết cho bài toán nghịch đảo
    del result["solution"]
    del result["matrix_B"]
    del result["vector_d"]

    return result