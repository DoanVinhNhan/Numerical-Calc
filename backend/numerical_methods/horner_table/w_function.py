# backend/numerical_methods/horner_table/w_function.py
import numpy as np
from backend.numerical_methods.horner_table.reverse_horner import reverse_horner

def calculate_w_function(roots):
    """
    Tính đa thức w(x) = (x - x_0)(x - x_1)...(x - x_n) bằng cách
    sử dụng lặp lại phương pháp nhân Horner.
    
    Parameters:
        roots (list of float): Danh sách các nghiệm x_i.
    
    Returns:
        dict: Chứa các bước trung gian và hệ số của đa thức cuối cùng.
    """
    if len(roots) == 0:
        raise ValueError("Danh sách nghiệm không được rỗng.")
    
    # Bắt đầu với w_0(x) = 1
    current_coeffs = [1.0]
    steps = []

    # w_{k+1}(x) = w_k(x) * (x - x_k)
    for i, root in enumerate(roots):
        step_result = reverse_horner(current_coeffs, root)
        
        steps.append({
            "step_index": i,
            "w_k_coeffs": current_coeffs,
            "root": root,
            "reverse_table": step_result['reverse_table'],
            "w_k_plus_1_coeffs": step_result['coeffs']
        })
        
        current_coeffs = step_result['coeffs']
        
    return {
        "steps": steps,
        "final_coeffs": current_coeffs,
        "roots": roots
    }