# backend/numerical_methods/root_finding/newton.py
import numpy as np

def newton_method(f, f_prime, f_double_prime, a, b, x0, mode, value, stop_condition, max_iter=200):
    """
    Tìm nghiệm của f(x) = 0 bằng phương pháp Newton (Tiếp tuyến).
    """
    steps = []

    # 1. Kiểm tra điều kiện hội tụ (f', f'' không đổi dấu)
    try:
        x_check = np.linspace(a, b, 20)
        fp_signs = np.sign([f_prime(x) for x in x_check if abs(f_prime(x)) > 1e-9])
        fpp_signs = np.sign([f_double_prime(x) for x in x_check if abs(f_double_prime(x)) > 1e-9])
        
        if len(set(fp_signs)) > 1 or len(set(fpp_signs)) > 1:
            raise ValueError("Điều kiện hội tụ: f'(x) và f''(x) phải không đổi dấu trên [a, b].")
    except Exception as e:
        raise ValueError(f"Không thể kiểm tra đạo hàm trên khoảng [a, b]. Lỗi: {e}")

    # 2. Tính các hằng số m1, M2
    try:
        x_range = np.linspace(a, b, 500)
        f_prime_values = np.abs([f_prime(x) for x in x_range])
        f_double_prime_values = np.abs([f_double_prime(x) for x in x_range])
        m1 = np.min(f_prime_values)
        M2 = np.max(f_double_prime_values)
        if m1 < 1e-12:
            raise ValueError("Đạo hàm f'(x) có giá trị gần bằng 0 trong khoảng, công thức sai số không đáng tin cậy.")
    except Exception as e:
        raise ValueError(f"Không thể tính m1, M2 trên khoảng [a, b]. Lỗi: {e}")
    
    # 4. Quá trình lặp
    x_k = x0
    iterations_to_run = int(value) if mode == 'iterations' else max_iter
    done = False
    
    for k in range(iterations_to_run):
        f_xk = f(x_k)
        df_xk = f_prime(x_k)
        
        if abs(df_xk) < 1e-12:
            raise ValueError(f"Đạo hàm bằng 0 tại x = {x_k}. Không thể tiếp tục.")

        x_k_plus_1 = x_k - f_xk / df_xk
        
        # Kiểm tra điểm lặp có nằm ngoài khoảng không
        if not (a <= x_k_plus_1 <= b):
            steps.append({'k': k + 1, 'xn': x_k, 'fxn': f_xk, "dfxn": df_xk})
            raise ValueError(f"Điểm lặp x_{k+1} = {x_k_plus_1:.6f} nằm ngoài khoảng [{a}, {b}].")
            
        step_info = {'k': k + 1, 'xn': x_k, 'fxn': f_xk, "dfxn": df_xk}
        
        # Đánh giá sai số và kiểm tra điều kiện dừng
        tol = float(value)
        
        if mode == 'absolute_error':
            error = (M2 / (2 * m1)) * (x_k_plus_1 - x_k)**2 if stop_condition == 'xn_x_prev' else np.abs(f(x_k_plus_1)) / m1
            step_info['error'] = error
            if error < tol: done = True
        elif mode == 'relative_error':
            if abs(x_k_plus_1) < 1e-12:
                error = float('inf')
            else:
                error = (M2 / (2 * m1)) * ((x_k_plus_1 - x_k)**2) / abs(x_k_plus_1) if stop_condition == 'xn_x_prev' else np.abs(f(x_k_plus_1)) / (m1 * abs(x_k_plus_1))
            step_info['error'] = error
            if error < tol: done = True

        steps.append(step_info)
        x_k = x_k_plus_1
        
        if done or (mode == 'iterations' and k + 1 >= iterations_to_run):
            break

    if not done and mode != 'iterations':
        raise ValueError(f"Phương pháp không hội tụ sau {iterations_to_run} lần lặp.")

    return {"solution": x_k, "iterations": len(steps), "steps": steps, "m1": m1, "M2": M2, "x0": x0}