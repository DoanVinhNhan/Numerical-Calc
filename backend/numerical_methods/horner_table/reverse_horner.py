# backend/numerical_methods/horner_table/reverse_horner.py
import numpy as np

def reverse_horner(coeffs, root):
    """
    Bảng nhân Horner P(x)*(x-c).
    Parameters:
        coeffs (list of float): Hệ số của đa thức, từ bậc cao nhất đến bậc thấp nhất.
        root (float): Giá trị của root trong (x - root).
    Returns:
        {
            "reverse_table": Bảng nhân Horner.
            "coeffs": Hệ số của đa thức mới.
        }
    """
    if len(coeffs) == 0:
        raise ValueError("Coefficient list cannot be empty.")
    
    n = len(coeffs)
    # Khởi tạo mảng hệ số mới với kích thước n + 1
    new_coeffs = np.zeros(n + 1)
    # Khởi tạo bảng Horner với kích thước phù hợp
    reverse_table = np.zeros((3, n + 1), dtype=float)
    
    # Chuẩn bị dòng đầu tiên của bảng bằng cách thêm 0 vào cuối hệ số gốc
    padded_coeffs = np.append(coeffs, 0)
    reverse_table[0, :] = padded_coeffs

    # Hệ số đầu tiên của đa thức mới bằng hệ số đầu tiên của đa thức cũ
    new_coeffs[0] = coeffs[0]
    reverse_table[2, 0] = new_coeffs[0]
    
    # Vòng lặp tính toán các hệ số còn lại
    for i in range(1, n + 1):
        val_to_add = -root * coeffs[i - 1]
        reverse_table[1, i] = val_to_add
        new_coeffs[i] = padded_coeffs[i] + val_to_add
        reverse_table[2, i] = new_coeffs[i]
        
    return {
        "reverse_table": reverse_table.tolist(),
        "coeffs": new_coeffs.tolist()
    }