# backend/numerical_methods/linear_algebra/inverse/jacobi_inverse.py
import numpy as np
from backend.utils.helpers import zero_small

def jacobi_inverse(A, x0_method='method1', tol=1e-5, max_iter=100):
    """
    Tìm ma trận nghịch đảo gần đúng bằng phương pháp lặp Jacobi.
    (Phiên bản đã sửa lỗi công thức sai số và cảnh báo)
    """
    n = A.shape[0]
    if n != A.shape[1]:
        raise ValueError("Ma trận phải là ma trận vuông.")

    diag_elements = np.diag(A)
    if np.any(np.isclose(diag_elements, 0)):
        raise ValueError("Ma trận có phần tử trên đường chéo chính bằng 0.")

    D_inv = np.diag(1.0 / diag_elements)
    B = np.eye(n) - D_inv @ A

    # Xác định chuẩn và đưa ra cảnh báo nếu cần
    diag_abs = np.abs(diag_elements)
    row_sum = np.sum(np.abs(A), axis=1) - diag_abs
    is_row_dominant = np.all(diag_abs > row_sum)
    norm = np.inf if is_row_dominant else 1
    norm_used_str = "infinity" if norm == np.inf else "1"
    
    contraction_coefficient = np.linalg.norm(B, norm)
    warning_message = None
    if contraction_coefficient >= 1:
        norm_symbol = '∞' if norm == np.inf else '₁'
        warning_message = (
            f"CẢNH BÁO: Điều kiện hội tụ có thể không thỏa mãn "
            f"(||B||{norm_symbol} = {contraction_coefficient:.4f} ≥ 1). "
            "Kết quả có thể không chính xác."
        )

    # Chọn X0
    x0_options = {
        'method1': ("X₀ = Aᵀ / ||A||₂²", A.T / (np.linalg.norm(A, 2) ** 2)),
        'method2': ("X₀ = Aᵀ / (||A||₁·||A||∞)", A.T / (np.linalg.norm(A, 1) * np.linalg.norm(A, np.inf)))
    }
    x0_label, X_k = x0_options[x0_method]

    iterations_data = []
    
    # Áp dụng công thức sai số hậu nghiệm
    stopping_factor = None
    if contraction_coefficient < 1:
        stopping_factor = contraction_coefficient / (1 - contraction_coefficient)

    for i in range(max_iter):
        X_k_plus_1 = B @ X_k + D_inv
        diff_norm = np.linalg.norm(X_k_plus_1 - X_k, norm)
        
        # Sử dụng công thức sai số đã tính
        if stopping_factor is not None:
            # Dùng công thức sai số hậu nghiệm khi q < 1
            estimated_error = stopping_factor * diff_norm
        else:
            # Dùng sai số thường khi q >= 1
            estimated_error = diff_norm
        
        iterations_data.append({ "k": i + 1, "x_k": X_k_plus_1, "error": estimated_error, "diff_norm": diff_norm })
        
        if estimated_error < tol:
            return {
                "status": "success", "inverse": zero_small(X_k_plus_1, tol), "iterations": i + 1,
                "iterations_data": iterations_data, "x0_matrix": X_k, "x0_label": x0_label,
                "contraction_coefficient": contraction_coefficient, "norm_used": norm_used_str,
                "is_row_dominant": is_row_dominant, "warning_message": warning_message
            }
        
        X_k = X_k_plus_1
        
    raise ValueError(f"Phương pháp không hội tụ sau {max_iter} lần lặp.")