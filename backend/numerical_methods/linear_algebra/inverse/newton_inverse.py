# backend/numerical_methods/linear_algebra/inverse/newton_inverse.py
import numpy as np
from backend.utils.helpers import zero_small

def newton_inverse(A, tol=1e-5, max_iter=100, x0_method='method1'):
    """
    Tìm ma trận nghịch đảo gần đúng bằng phương pháp lặp Newton.
    Xₖ₊₁ = Xₖ(2E - AXₖ)
    """
    n = A.shape[0]
    if n != A.shape[1]:
        raise ValueError("Ma trận phải là ma trận vuông.")
    if np.isclose(np.linalg.det(A), 0):
        raise ValueError("Ma trận suy biến (det(A) ≈ 0), không có nghịch đảo.")

    E = np.identity(n)
    
    # Chọn X₀ ban đầu và tính hệ số co q
    X0_1 = A.T / (np.linalg.norm(A, 2)**2)
    q1 = np.linalg.norm(E - A @ X0_1, 2)
    
    X0_2 = A.T / (np.linalg.norm(A, 1) * np.linalg.norm(A, np.inf))
    q2 = np.linalg.norm(E - A @ X0_2, 2)
    
    x0_label = ""
    if x0_method == 'method1':
        X_k = X0_1
        q = q1
        x0_label = "X₀ = Aᵀ / ||A||₂²"
    elif x0_method == 'method2':
        X_k = X0_2
        q = q2
        x0_label = "X₀ = Aᵀ / (||A||₁·||A||∞)"
    else: # Mặc định tự động chọn
        if q1 < q2:
            X_k = X0_1
            q = q1
            x0_label = "Tự động chọn X₀ = Aᵀ / ||A||₂²"
        else:
            X_k = X0_2
            q = q2
            x0_label = "Tự động chọn X₀ = Aᵀ / (||A||₁·||A||∞)"

    if q >= 1:
        raise ValueError(f"Điều kiện hội tụ không thỏa mãn với {x0_label} (hệ số co q = {q:.4f} >= 1).")

    iterations_data = []
    
    for i in range(1, max_iter + 1):
        X_k_plus_1 = X_k @ (2 * E - A @ X_k)
        
        # Luôn sử dụng chuẩn 2 cho phương pháp Newton
        diff_norm = np.linalg.norm(X_k_plus_1 - X_k, 2)
        
        # Đánh giá sai số hậu nghiệm
        estimated_error = (q / (1 - q)) * diff_norm
        
        iterations_data.append({
            "k": i,
            "x_k": X_k_plus_1,
            "diff_norm": diff_norm,
            "estimated_error": estimated_error
        })
        
        if estimated_error < tol:
            return {
                "status": "success",
                "inverse": zero_small(X_k_plus_1, tol),
                "iterations": i,
                "iterations_data": iterations_data,
                "contraction_coefficient": q,
                "x0_label": x0_label,
                "initial_matrix": X_k,
                "check_matrix": A @ X_k_plus_1
            }
        
        X_k = X_k_plus_1

    raise ValueError(f"Phương pháp không hội tụ sau {max_iter} lần lặp. Sai số cuối cùng là {estimated_error:.2e}.")