# backend/numerical_methods/root_finding/secant.py
import numpy as np

def secant_method(f, f_prime, f_double_prime, a, b, mode, value, stop_condition, max_iter=200):
    """
    Tìm nghiệm của f(x) = 0 bằng phương pháp Dây cung (Secant).
    """
    steps = []

    # 1. Kiểm tra các điều kiện hội tụ ban đầu
    fa = f(a)
    fb = f(b)
    if fa * fb >= 0:
        raise ValueError(f"Điều kiện f(a)f(b) < 0 không thỏa mãn. f(a)={fa:.4f}, f(b)={fb:.4f}")

    try:
        x_check = np.linspace(a, b, 20)
        fp_signs = np.sign([f_prime(x) for x in x_check if abs(f_prime(x)) > 1e-9])
        fpp_signs = np.sign([f_double_prime(x) for x in x_check if abs(f_double_prime(x)) > 1e-9])
        
        if len(set(fp_signs)) > 1 or len(set(fpp_signs)) > 1:
            raise ValueError("Điều kiện hội tụ f'(x) và f''(x) không đổi dấu trên [a, b] không thỏa mãn.")
    except Exception as e:
        raise ValueError(f"Không thể kiểm tra đạo hàm trên khoảng [a, b]. Lỗi: {e}")

    # 2. Chọn điểm cố định d (điểm Fourier) và điểm lặp x0
    if f(a) * f_double_prime(a) > 0:
        d, x0 = a, b
    elif f(b) * f_double_prime(b) > 0:
        d, x0 = b, a
    else:
        # Nếu không thỏa mãn, thử chọn điểm có f'' cùng dấu với f tại điểm đó
        # Đây là một nới lỏng điều kiện hội tụ chặt
        x_mid = (a+b)/2
        if f(a) * f_double_prime(x_mid) > 0: d,x0 = a,b
        elif f(b) * f_double_prime(x_mid) > 0: d,x0 = b,a
        else: raise ValueError("Không tìm thấy điểm Fourier phù hợp để đảm bảo hội tụ.")

    # 3. Tính các hằng số m1, M1
    try:
        x_range = np.linspace(a, b, 500)
        f_prime_values = np.abs([f_prime(x) for x in x_range])
        m1 = np.min(f_prime_values)
        M1 = np.max(f_prime_values)
        if m1 < 1e-12:
            raise ValueError("Đạo hàm f'(x) có giá trị gần bằng 0 trong khoảng, công thức sai số không đáng tin cậy.")
    except Exception as e:
        raise ValueError(f"Không thể tính m1, M1 trên khoảng [a, b]. Lỗi: {e}")

    # 4. Quá trình lặp
    x_curr = x0
    iterations_to_run = int(value) if mode == 'iterations' else max_iter
    
    for i in range(iterations_to_run):
        f_curr = f(x_curr)
        f_d = f(d)
        step_info = {"n": i + 1, "xn": x_curr, "fxn": f_curr}
        
        x_prev = x_curr
        denominator = f_curr - f_d
        if abs(denominator) < 1e-15:
            raise ValueError("Mẫu số f(x_n) - f(d) tiến tới 0, không thể tiếp tục.")
            
        x_curr = x_curr - (f_curr * (x_curr - d)) / denominator
        
        # Đánh giá sai số và kiểm tra điều kiện dừng
        tol = float(value)
        done = False
        
        if mode == 'absolute_error':
            error = ((M1 - m1) / m1) * np.abs(x_curr - x_prev) if stop_condition == 'xn_x_prev' else np.abs(f_curr) / m1
            step_info['error'] = error
            if error < tol: done = True
        elif mode == 'relative_error':
            if abs(x_curr) < 1e-12:
                error = float('inf')
            else:
                error = ((M1 - m1) / m1) * np.abs(x_curr - x_prev) / np.abs(x_curr) if stop_condition == 'xn_x_prev' else np.abs(f_curr) / (m1 * np.abs(x_curr))
            step_info['error'] = error
            if error < tol: done = True
        
        steps.append(step_info)
        if done or (mode == 'iterations' and i + 1 >= iterations_to_run):
            break
            
    if i >= max_iter -1 and not done and mode != 'iterations':
        raise ValueError(f"Không hội tụ sau {max_iter} lần lặp.")

    return {"solution": x_curr, "steps": steps, "iterations": len(steps), "m1": m1, "M1": M1, "d": d, "x0": x0}