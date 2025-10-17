#backend/numerical_methods/horner_table/all_derivatives.py
import numpy as np
from backend.numerical_methods.horner_table.all_derivatives import all_derivatives

def change_variables(coeffs, a, b):
    """
    Đổi biến hệ số đa thức từ biến x sang biến t theo công thức:
    t = ax+b
    Parameters:
        coeffs (list of float): Hệ số của đa thức theo biến x, từ bậc cao nhất đến bậc thấp nhất.
        a (float): Hệ số của biến t trong công thức đổi biến.
        b (float): Hằng số trong công thức đổi biến.
    Returns:
        dict:{
            step:{
                "division_table": Bảng chia horner tại từng bước
                "coeffs": Hệ số của đa thức thương tại mỗi bước}
            },
            "variables_coeffs": Hệ số của đa thức sau khi đổi biến
        }
    """
    if len(coeffs) == 0:
        raise ValueError("Coefficient list cannot be empty.")
    if np.isclose(a, 0):
        raise ValueError("Coefficient 'a' cannot be zero.")
    
    root = -b / a
    results = all_derivatives(coeffs, root, len(coeffs) - 1)
    return {
        "steps": results['steps'],
        "variables_coeffs": results['values'][::-1]
    }