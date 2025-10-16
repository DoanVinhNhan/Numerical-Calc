#backend/numerical_methods/horner_table/all_derivatives.py
import numpy as np
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division

def all_derivatives(coeffs, root, order):
    """
    Tính các hệ số của đa thức và các đạo hàm tại một điểm sử dụng phương pháp Horner mở rộng.
    
    Parameters:
        coeffs (list of float): Hệ số của đa thức, từ bậc cao nhất đến bậc thấp nhất.
        root (float): Giá trị tại đó tính đa thức và các đạo hàm.
        order (int): Số bậc đạo hàm cần tính (bao gồm cả đa thức gốc).
    
    Returns:
        dict:{
            step:{
                "division_table": Bảng chia horner tại từng bước
                "coeffs": Hệ số của đa thức thương tại mỗi bước}
            },
            "values": Danh sách b_0 của các đa thức tại `root`
            "derivatives": Danh sách giá trị của đa thức và các đạo hàm tại `root`
        }
    """
    if order < 0:
        raise ValueError("Order must be a non-negative integer.")
    if len(coeffs) == 0:
        raise ValueError("Coefficient list cannot be empty.")
    
    results = {}
    current_coeffs = np.array(coeffs, dtype=float)
    values = []
    derivatives_value = []
    
    for n in range(order + 1):
        division_result = synthetic_division(current_coeffs, root)
        results[f"step_{n}"] = {
            "division_table": division_result['division_table'].tolist(),
            "coeffs": division_result['quotient_coeffs'].tolist()
        }
        values.append(division_result['value'])
        derivatives_value.append(division_result['value'] * np.math.factorial(n))
        current_coeffs = division_result['quotient_coeffs']
        if len(current_coeffs) == 0 or np.all(np.isclose(current_coeffs, 0)):
            break
    
    return {
        "steps": results,
        "values": values,
        "derivatives": derivatives_value
    }