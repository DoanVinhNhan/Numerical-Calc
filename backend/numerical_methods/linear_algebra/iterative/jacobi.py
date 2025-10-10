# backend/numerical_methods/linear_algebra/iterative/jacobi.py
import numpy as np
from backend.utils.helpers import zero_small

def jacobi(A, b, x0, tol=1e-5, max_iter=100):
    """
    Giải hệ phương trình Ax=b bằng phương pháp lặp Jacobi.
    """
    n = A.shape[0]
    if n != A.shape[1]:
        raise ValueError("Ma trận A phải là ma trận vuông.")
    if b.ndim == 1:
        b = b.reshape(-1, 1)
    if x0.ndim == 1:
        x0 = x0.reshape(-1, 1)

    diag_elements = np.diag(A)
    if np.any(np.isclose(diag_elements, 0)):
        raise ValueError("Ma trận có phần tử trên đường chéo chính bằng 0, không thể thực hiện phép lặp.")

    # Kiểm tra điều kiện chéo trội
    diag_abs = np.abs(diag_elements)
    row_sum = np.sum(np.abs(A), axis=1) - diag_abs
    col_sum = np.sum(np.abs(A), axis=0) - diag_abs
    is_row_dominant = np.all(diag_abs > row_sum)
    is_col_dominant = np.all(diag_abs > col_sum)

    if not is_row_dominant and not is_col_dominant:
        raise ValueError("Ma trận không chéo trội hàng hoặc cột. Hội tụ không được đảm bảo.")

    # Thiết lập ma trận lặp B và vector d
    T = np.diag(1.0 / diag_elements)
    B = np.identity(n) - T @ A
    d = T @ b
    
    # Xác định chuẩn và hệ số co để đánh giá sai số
    if is_row_dominant:
        norm = np.inf
        norm_used = "infinity"
        contraction_coefficient = np.linalg.norm(B, norm)
        stopping_factor = contraction_coefficient / (1 - contraction_coefficient)
    else: # is_col_dominant
        norm = 1
        norm_used = "1"
        B1_conv = np.identity(n) - A @ T
        contraction_coefficient = np.linalg.norm(B1_conv, norm)
        lambda_factor = np.max(diag_abs) / np.min(diag_abs)
        stopping_factor = lambda_factor * contraction_coefficient / (1 - contraction_coefficient)

    # Quá trình lặp
    x_k = x0.copy()
    iterations_data = []
    
    for i in range(max_iter):
        x_k_plus_1 = B @ x_k + d
        diff_norm = np.linalg.norm(x_k_plus_1 - x_k, norm)
        estimated_error = stopping_factor * diff_norm

        iterations_data.append({
            "k": i + 1,
            "x_k": x_k_plus_1,
            "error": estimated_error,
            "diff_norm": diff_norm
        })
        
        if estimated_error < tol:
            return {
                "status": "success",
                "solution": zero_small(x_k_plus_1, tol),
                "iterations": i + 1,
                "iterations_data": iterations_data,
                "contraction_coefficient": contraction_coefficient,
                "norm_used": norm_used,
                "is_row_dominant": is_row_dominant,
                "is_col_dominant": is_col_dominant,
                "matrix_B": zero_small(B, tol),
                "vector_d": zero_small(d, tol)
            }
        
        x_k = x_k_plus_1
    
    # Nếu không hội tụ
    raise ValueError(f"Phương pháp không hội tụ sau {max_iter} lần lặp.")