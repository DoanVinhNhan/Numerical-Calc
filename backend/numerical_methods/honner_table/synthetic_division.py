#backend/numerical_methods/honner_table/synthetic_division.py
import numpy as np

def synthetic_division(coeffs, root):
    """
    Thực hiện phép chia tổng hợp (synthetic division) của đa thức với hệ số `coeffs`
    cho đa thức bậc nhất (x - root).

    Parameters:
        coeffs (list or np.ndarray): Hệ số của đa thức, từ bậc cao nhất đến bậc thấp nhất.
        root (float): Nghiệm để chia.

    Returns:
        division_table: Bảng chia honner
        dict: Kết quả bao gồm hệ số của đa thức thương
        value: Giá trị của đa thức tại `root`.
    """
    n = len(coeffs)
    if n==0:
        raise ValueError("Hệ số đa thức không được rỗng.")
    division_table = np.zeros((3, n), dtype=float)
    division_table[0, :] = coeffs
    division_table[1, 0] = 0.0
    division_table[2, 0] = coeffs[0]
    for i in range(1, n):
        division_table[1, i] = division_table[2, i-1] * root
        division_table[2, i] = division_table[0, i] + division_table[1, i]
    
    quotient_coeffs = division_table[2, :-1]
    value = division_table[2, -1]
    return {'division_table': division_table,
            'quotient_coeffs': quotient_coeffs,
            'value': value}
