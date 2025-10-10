# backend/numerical_methods/linear_algebra/iterative/gauss_seidel.py
# Chức năng: Cung cấp thuật toán lặp Gauss-Seidel.
import numpy as np
from backend.utils.helpers import zero_small

def gauss_seidel(A, b, x0, tol=1e-5, max_iter=100):
    # Giải hệ Ax=b bằng phương pháp Gauss-Seidel.
    n = A.shape[0]
    if n != A.shape[1]:
        raise ValueError("Ma trận A phải là ma trận vuông.")
    if b.ndim == 1:
        b = b.reshape(-1, 1)
    if x0.ndim == 1:
        x0 = x0.reshape(-1, 1)

    diag_elements = np.diag(A)
    if np.any(np.isclose(diag_elements, 0)):
        raise ValueError("Ma trận có phần tử trên đường chéo chính bằng 0.")

    diag_abs = np.abs(diag_elements)
    row_sum_off_diag = np.sum(np.abs(A), axis=1) - diag_abs
    col_sum_off_diag = np.sum(np.abs(A), axis=0) - diag_abs
    is_row_dominant = np.all(diag_abs > row_sum_off_diag)
    is_col_dominant = np.all(diag_abs > col_sum_off_diag)

    if not is_row_dominant and not is_col_dominant:
        raise ValueError("Ma trận không chéo trội hàng hoặc cột. Hội tụ không được đảm bảo.")

    s, q, norm = 0, 0, 0
    if is_row_dominant:
        norm = np.inf
        s = 0
        q_num = np.zeros(n)
        q_den = np.zeros(n)
        for i in range(n):
            q_num[i] = np.sum(np.abs(A[i, :i]))
            q_den[i] = np.abs(A[i, i]) - np.sum(np.abs(A[i, i+1:]))
        q_den[np.isclose(q_den, 0)] = 1e-15
        q = np.max(q_num / q_den)
    else: # is_col_dominant
        norm = 1
        s_num = np.zeros(n)
        for j in range(n):
            s_num[j] = np.sum(np.abs(A[j+1:, j]))
        s = np.max(s_num / diag_abs)
        q_num = np.zeros(n)
        q_den = np.zeros(n)
        for j in range(n):
            q_num[j] = np.sum(np.abs(A[:j, j]))
            q_den[j] = np.abs(A[j, j]) - np.sum(np.abs(A[j+1:, j]))
        q_den[np.isclose(q_den, 0)] = 1e-15
        q = np.max(q_num / q_den)
    
    denominator = (1 - s) * (1 - q)
    if np.isclose(denominator, 0):
        raise ValueError(f"Hệ số q={q:.4f} hoặc s={s:.4f} không hợp lệ, gây lỗi chia cho 0.")
    stopping_factor = q / denominator

    x_k = x0.copy().astype(float)
    iterations_data = []
    
    for i in range(max_iter):
        x_prev = x_k.copy()
        for j in range(n):
            sum1 = np.dot(A[j, :j], x_k[:j, :])
            sum2 = np.dot(A[j, j+1:], x_prev[j+1:, :])
            x_k[j, :] = (b[j, :] - sum1 - sum2) / A[j, j]
        
        diff_norm = np.linalg.norm(x_k - x_prev, norm)
        estimated_error = stopping_factor * diff_norm
        
        iterations_data.append({
            "k": i + 1,
            "x_k": x_k,
            "error": estimated_error,
            "diff_norm": diff_norm
        })
        
        if estimated_error < tol:
            return {
                "status": "success",
                "solution": zero_small(x_k, tol),
                "iterations": i + 1,
                "iterations_data": iterations_data,
                "coeff_q": q,
                "coeff_s": s,
                "norm_used": "infinity" if norm == np.inf else "1",
                "is_row_dominant": is_row_dominant,
            }
        
    raise ValueError(f"Phương pháp không hội tụ sau {max_iter} lần lặp.")