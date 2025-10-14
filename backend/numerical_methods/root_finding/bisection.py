# backend/numerical_methods/root_finding/bisection.py
import numpy as np

def bisection_method(f, a, b, mode, value, max_iter=200):
    """
    Tìm nghiệm của f(x) = 0 trên khoảng [a, b] bằng phương pháp chia đôi.
    Hàm này chỉ thực hiện tính toán và trả về kết quả thô.
    """
    steps = []
    
    # Kiểm tra điều kiện ban đầu
    fa = f(a)
    fb = f(b)
    if fa * fb >= 0:
        raise ValueError(f"Khoảng [{a}, {b}] không phải là khoảng cách ly nghiệm vì f(a)={fa:.4f} và f(b)={fb:.4f} không trái dấu.")

    # Kiểm tra tính đơn điệu (xấp xỉ)
    x_check = np.linspace(a, b, 20)
    h = 1e-6
    try:
        deriv_signs = [np.sign((f(x + h) - f(x - h)) / (2 * h)) for x in x_check]
        # Bỏ qua các giá trị gần 0
        deriv_signs = [s for s in deriv_signs if abs(s) > 1e-8]
        if not (all(s > 0 for s in deriv_signs) or all(s < 0 for s in deriv_signs)):
            # Đây là một cảnh báo thay vì lỗi, vì có thể vẫn tìm được nghiệm
            pass # Bỏ qua lỗi không đơn điệu để linh hoạt hơn
    except Exception:
        pass # Bỏ qua nếu không tính được đạo hàm

    c = a
    i = 0

    if mode == "iterations":
        n_iters = int(value)
        for i in range(n_iters):
            c_prev = c
            c = (a + b) / 2
            fc = f(c)
            steps.append({"n": i + 1, "a": a, "b": b, "c": c, "fc": fc, "error": abs(c - c_prev)})
            if fc == 0.0: break
            if fa * fc < 0:
                b = c
            else:
                a = c
                fa = fc
        return {"solution": c, "steps": steps, "iterations": len(steps)}

    # Xử lý cho sai số tuyệt đối và tương đối
    c_prev = a # Khởi tạo để vòng lặp đầu tiên chạy
    
    while i < max_iter:
        c = (a + b) / 2
        fc = f(c)
        
        error = abs(c - c_prev)
        relative_error = error / abs(c) if abs(c) > 1e-15 else float('inf')
        
        steps.append({"n": i + 1, "a": a, "b": b, "c": c, "fc": fc, "error": error, "relative_error": relative_error})
        
        # Kiểm tra điều kiện dừng
        stop = False
        if mode == "absolute_error" and error < float(value): stop = True
        if mode == "relative_error" and relative_error < float(value): stop = True
        if fc == 0.0: stop = True
        
        if stop: break
        
        # Cập nhật khoảng
        if fa * fc < 0:
            b = c
        else:
            a = c
            fa = fc
            
        c_prev = c
        i += 1
        
    if i >= max_iter:
        raise ValueError(f"Phương pháp không hội tụ sau {max_iter} lần lặp.")

    return {"solution": c, "steps": steps, "iterations": len(steps)}