import numpy as np
from backend.utils.helpers import zero_small

def simple_iteration(B, d, x0, tol=1e-5, max_iter=100, norm_choice='inf'):
    # Giải hệ phương trình x = Bx + d bằng phương pháp lặp đơn.
    if B.shape[0] != B.shape[1]:
        raise ValueError(f"Ma trận B phải là ma trận vuông. Kích thước hiện tại: {B.shape}")
    if d.ndim == 1:
        d = d.reshape(-1, 1)
    if x0.ndim == 1:
        x0 = x0.reshape(-1, 1)
    if B.shape[1] != d.shape[0]:
        raise ValueError(f"Số cột của B ({B.shape[1]}) không khớp với số hàng của d ({d.shape[0]})")
    if d.shape != x0.shape:
        raise ValueError(f"Kích thước của d ({d.shape}) và x0 ({x0.shape}) phải giống nhau.")

    norm = np.inf if norm_choice == 'inf' else 1
    norm_B = np.linalg.norm(B, norm)
    
    warning_message = None
    if norm_B >= 1:
        norm_symbol = '∞' if norm == np.inf else '₁'
        warning_message = (
            f"CẢNH BÁO: Điều kiện hội tụ có thể không thỏa mãn. "
            f"Chuẩn ||B||{norm_symbol} = {norm_B:.4f} ≥ 1. "
            "Quá trình lặp có thể không hội tụ."
        )

    # Điều kiện dừng
    stopping_threshold = tol
    if norm_B < 1:
        stopping_threshold = abs((1 - norm_B) / norm_B) * tol

    x_k = x0.copy()
    iterations_data = [{'k': 0, 'x_k': x_k, 'error': None}]
    
    for k in range(1, max_iter + 1):
        x_k_plus_1 = B @ x_k + d
        error = np.linalg.norm(x_k_plus_1 - x_k, norm)
        x_k = x_k_plus_1
        
        iterations_data.append({'k': k, 'x_k': x_k, 'error': error})
        
        if error < stopping_threshold:
            return {
                "status": "success",
                "solution": zero_small(x_k, tol),
                "iterations": k,
                "iterations_data": iterations_data,
                "norm_B": norm_B,
                "warning_message": warning_message,
                "norm_used": norm_choice,
                "stopping_threshold": stopping_threshold
            }

    raise ValueError(f"Không hội tụ sau {max_iter} lần lặp. Sai số cuối cùng là {error:.2e}.")