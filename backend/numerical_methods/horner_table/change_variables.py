# backend/numerical_methods/horner_table/change_variables.py
import numpy as np
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division

def change_variables(coeffs_t, a, b):
    """
    Đổi biến đa thức P(x) thành Q(t) với t = ax + b.
    Sử dụng phương pháp chia Horner lặp (khai triển Taylor).

    Parameters:
        coeffs_t (list of float): Hệ số của đa thức P(x) ban đầu, từ bậc cao nhất.
                                  Lưu ý: Mặc dù tên là coeffs_t, nhưng nó thực sự
                                  là hệ số của đa thức gốc P(x).
        a (float): Hệ số của x trong t = ax + b.
        b (float): Hằng số tự do trong t = ax + b.

    Returns:
        dict: Chứa các bước tính toán và hệ số của đa thức Q(t).
              - steps: Danh sách các bước chia Horner lặp.
              - variables_coeffs: Danh sách hệ số của đa thức Q(t) theo biến t,
                                    từ bậc cao nhất đến thấp nhất.
    """
    if len(coeffs_t) == 0:
        raise ValueError("Coefficient list cannot be empty.")
    if np.isclose(a, 0):
        raise ValueError("Coefficient 'a' cannot be zero.")

    n = len(coeffs_t) - 1
    x0 = -b / a
    a_prime = 1.0 / a

    steps = []
    current_coeffs_np = np.array(coeffs_t, dtype=float)
    taylor_coeffs_dk = []

    for k in range(n + 1):
        coeffs_before_division = current_coeffs_np.tolist()

        horner_result = synthetic_division(current_coeffs_np, x0)
        remainder = horner_result['value'] 
        quotient_coeffs_np = horner_result['quotient_coeffs'] 

        taylor_coeffs_dk.append(remainder)

        steps.append({
            "step_index": k,
            "polynomial_coeffs_before": coeffs_before_division,
            "division_table": horner_result['division_table'].tolist(),
            "remainder_dk": remainder,
            "quotient_coeffs": quotient_coeffs_np.tolist()
        })

        current_coeffs_np = quotient_coeffs_np
        if current_coeffs_np.size == 0:
            taylor_coeffs_dk.extend([0.0] * (n - k))
            break


    coeffs_q_reverse = [taylor_coeffs_dk[k] * (a_prime**k) for k in range(n + 1)]


    final_coeffs_q = coeffs_q_reverse[::-1]

    return {
        "steps": steps,
        "variables_coeffs": final_coeffs_q
    }