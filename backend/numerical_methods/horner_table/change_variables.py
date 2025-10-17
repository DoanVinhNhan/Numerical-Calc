# backend/numerical_methods/horner_table/change_variables.py
import numpy as np
from backend.numerical_methods.horner_table.reverse_horner import reverse_horner

def change_variables(coeffs_t, a, b):
    """
    Đổi biến đa thức P(t) thành P(x) với quan hệ t = ax + b.
    Parameters:
        coeffs_t (list of float): Hệ số của đa thức theo biến t.
        a (float): Hệ số của x.
        b (float): Hằng số tự do.
    Returns:
        dict: Chứa các bước tính toán và hệ số đa thức theo biến x.
    """
    if len(coeffs_t) == 0:
        raise ValueError("Coefficient list cannot be empty.")
    if np.isclose(a, 0):
        raise ValueError("Coefficient 'a' cannot be zero.")

    n = len(coeffs_t) - 1
    x0 = -b / a

    coeffs_d = [c * (a ** (n - i)) for i, c in enumerate(coeffs_t)]

    steps = []
    final_coeffs = [coeffs_d[0]]
    for i in range(1, n + 1):
        horner_result = reverse_horner(final_coeffs, x0)
        multiplied_coeffs = horner_result['coeffs']
        multiplied_coeffs[-1] += coeffs_d[i]
        final_coeffs = multiplied_coeffs

        steps.append({
            "horner_table": horner_result['reverse_table'],
            "added_coeff": coeffs_d[i],
            "coeffs": final_coeffs
        })
        
    return {
        "steps": steps,
        "variables_coeffs": final_coeffs
    }