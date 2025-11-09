# backend/numerical_methods/interpolation/inverse_interpolation.py
import numpy as np
from typing import List, Dict, Any
from backend.numerical_methods.interpolation.finite_difference import finite_differences
import math

def solve_inverse_iterative(
    x_nodes: List[float], 
    y_nodes: List[float], 
    y_bar: float, 
    epsilon: float, 
    method: str, 
    max_iter: int = 100
) -> Dict[str, Any]:
    """
    Giải bài toán nội suy ngược f(x) = y_bar bằng phương pháp lặp
    sử dụng đa thức Newton tiến hoặc lùi.
    """
    
    x = np.array(x_nodes, dtype=float)
    y = np.array(y_nodes, dtype=float)

    if len(x) != len(y):
        raise ValueError("Số lượng mốc x và giá trị y phải bằng nhau.")
    n_nodes = len(x)
    if n_nodes < 2:
        raise ValueError("Cần ít nhất 2 điểm nội suy.")

    # Sắp xếp các mốc
    sorted_indices = np.argsort(x)
    x = x[sorted_indices]
    y = y[sorted_indices]

    # Kiểm tra mốc cách đều
    h = x[1] - x[0]
    if not np.allclose(np.diff(x), h):
        raise ValueError("Phương pháp lặp nội suy ngược yêu cầu các mốc x phải cách đều nhau.")

    # Tính bảng sai phân
    fd_result = finite_differences(x.tolist(), y.tolist())
    fd_table = fd_result["finite_difference_table"]

    result = {}
    iteration_steps = []
    
    if method == 'forward':
        # --- NEWTON TIẾN ---
        x_start = x[0]
        y_start = y[0]
        # Lấy đường chéo trên cùng: y0, Δy0, Δ²y0, ...
        selected_diffs = [fd_table[i][i+1] for i in range(n_nodes)]
        
        if np.isclose(selected_diffs[1], 0): # selected_diffs[1] là Δy0
            raise ValueError(f"Sai phân cấp 1 (Δy₀ = {selected_diffs[1]:.2e}) bằng 0, không thể chia. Không thể dùng Newton Tiến.")

        t0 = (y_bar - y_start) / selected_diffs[1]
        
        def phi_forward(t: float) -> float:
            term_sum = 0.0
            t_prod = t * (t - 1)
            for k in range(2, n_nodes): # Bắt đầu từ Δ² (index 2 trong selected_diffs)
                factorial = math.factorial(k)
                term_sum += (selected_diffs[k] / factorial) * t_prod
                t_prod *= (t - (k - 1)) # t(t-1)(t-2), ...
            return (y_bar - y_start - term_sum) / selected_diffs[1]
        
        phi = phi_forward
        result["method_name"] = "Newton Tiến"
        result["formula_latex"] = f"t = \\frac{{1}}{{\\Delta y_0}} (\\bar{{y}} - y_0 - \\sum_{{k=2}}^{{{n_nodes-1}}} \\frac{{\\Delta^k y_0}}{{k!}} \\cdot w_k(t))"
        result["selected_diffs"] = selected_diffs[1:] # Trả về [Δy0, Δ²y0, ...]
        
    elif method == 'backward':
        # --- NEWTON LÙI ---
        x_start = x[-1] # x_n
        y_start = y[-1] # y_n
        # Lấy hàng cuối cùng: y_n, ∇y_n, ∇²y_n, ...
        selected_diffs = [fd_table[n_nodes-1][i+1] for i in range(n_nodes)]
        
        if np.isclose(selected_diffs[1], 0): # selected_diffs[1] là ∇y_n
            raise ValueError(f"Sai phân cấp 1 (∇yₙ = {selected_diffs[1]:.2e}) bằng 0, không thể chia. Không thể dùng Newton Lùi.")

        t0 = (y_bar - y_start) / selected_diffs[1]

        def phi_backward(t: float) -> float:
            term_sum = 0.0
            t_prod = t * (t + 1)
            for k in range(2, n_nodes): # Bắt đầu từ ∇² (index 2 trong selected_diffs)
                factorial = math.factorial(k)
                term_sum += (selected_diffs[k] / factorial) * t_prod
                t_prod *= (t + (k - 1)) # t(t+1)(t+2), ...
            return (y_bar - y_start - term_sum) / selected_diffs[1]

        phi = phi_backward
        result["method_name"] = "Newton Lùi"
        result["formula_latex"] = f"t = \\frac{{1}}{{\\nabla y_n}} (\\bar{{y}} - y_n - \\sum_{{k=2}}^{{{n_nodes-1}}} \\frac{{\\nabla^k y_n}}{{k!}} \\cdot w_k(t))"
        result["selected_diffs"] = selected_diffs[1:] # Trả về [∇y_n, ∇²y_n, ...]

    else:
        raise ValueError("Phương pháp không hợp lệ. Chỉ hỗ trợ 'forward' hoặc 'backward'.")

    # --- Quá trình lặp ---
    t_k = t0
    for i in range(max_iter):
        t_k_plus_1 = phi(t_k)
        error = abs(t_k_plus_1 - t_k)
        
        iteration_steps.append({
            "k": i + 1, 
            "t_k": t_k, 
            "t_k+1": t_k_plus_1, 
            "error": error
        })
        
        if error < epsilon:
            t_final = t_k_plus_1
            x_final = x_start + t_final * h
            
            result.update({
                "status": "success",
                "start_node": x_start,
                "h": h,
                "finite_difference_table": fd_table,
                "t0": t0,
                "iteration_table": iteration_steps,
                "t_final": t_final,
                "x_final": x_final
            })
            return result
            
        t_k = t_k_plus_1
        
    raise ValueError(f"Phương pháp lặp không hội tụ sau {max_iter} lần lặp. Sai số cuối cùng: {error:.2e}")