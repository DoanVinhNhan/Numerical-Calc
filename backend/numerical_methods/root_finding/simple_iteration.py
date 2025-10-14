# backend/numerical_methods/root_finding/simple_iteration.py
import numpy as np

def simple_iteration_method(phi, phi_prime, a, b, x0, mode, value, max_iter=200):
    """
    Tìm nghiệm của x = phi(x) bằng phương pháp lặp đơn.
    """
    # 1. Kiểm tra điều kiện cách ly nghiệm f(x) = phi(x) - x
    f = lambda x: phi(x) - x
    fa = f(a)
    fb = f(b)
    if fa * fb >= 0:
        raise ValueError(f'Khoảng [{a}, {b}] không phải là khoảng cách ly nghiệm vì f(a)={fa:.4f} và f(b)={fb:.4f} không trái dấu.')

    # 2. Kiểm tra điều kiện hội tụ q = max|phi'(x)|
    try:
        test_points = np.linspace(a, b, 200)
        q_vals = np.abs([phi_prime(p) for p in test_points])
        q = np.max(q_vals)
        if q >= 1:
            raise ValueError(f"Điều kiện hội tụ không thỏa mãn. Hệ số co q ≈ {q:.4f} >= 1.")
    except Exception as e:
        raise ValueError(f"Không thể tính đạo hàm của hàm lặp φ'(x) để xét điều kiện hội tụ. Lỗi: {e}")

    # 3. Quá trình lặp
    steps = []
    x_k = x0
    iterations_to_run = int(value) if mode == 'iterations' else max_iter
    done = False
    
    for k in range(iterations_to_run):
        x_k_plus_1 = phi(x_k)
        
        # Kiểm tra điểm lặp có nằm ngoài khoảng không
        if not (a <= x_k_plus_1 <= b):
            steps.append({'k': k + 1, 'xn': x_k, 'phixn': x_k_plus_1})
            raise ValueError(f"Điểm lặp x_{k+1} = {x_k_plus_1:.6f} nằm ngoài khoảng [{a}, {b}].")

        abs_diff = np.abs(x_k_plus_1 - x_k)
        error = (q / (1 - q)) * abs_diff if (1 - q) != 0 else float('inf')
        
        step_info = {
            'k': k + 1,
            'xn': x_k,
            'phixn': x_k_plus_1,
            'abs_diff': abs_diff,
            'error': error
        }
        steps.append(step_info)
        
        # Kiểm tra điều kiện dừng
        tol = float(value)
        if mode == 'absolute_error' and error < tol: done = True
        if mode == 'relative_error' and (error / abs(x_k_plus_1) if abs(x_k_plus_1) > 1e-12 else float('inf')) < tol: done = True
        
        x_k = x_k_plus_1
        
        if done or (mode == 'iterations' and k + 1 >= iterations_to_run):
            break

    if not done and mode != 'iterations':
        raise ValueError(f"Phương pháp không hội tụ sau {iterations_to_run} lần lặp.")

    return {"solution": x_k, "iterations": len(steps), "steps": steps, "q": q, "x0": x0}