# backend/api_formatters/horner_table.py
import numpy as np

def _format_poly_str(coeffs, variable='x'):
    """Tạo một chuỗi đa thức ở định dạng LaTeX từ danh sách các hệ số."""
    terms = []
    degree = len(coeffs) - 1
    if degree < 0:
        return "0"
        
    for i, c in enumerate(coeffs):
        if np.isclose(c, 0):
            continue
        
        power = degree - i
        
        sign = " - " if c < 0 else " + "
        c_abs = abs(c)
        
        if np.isclose(c_abs, 1) and power != 0:
            coeff_str = ""
        else:
            coeff_str = f"{c_abs:g}"

        if power > 1:
            var_str = f"{variable}^{{{power}}}"
        elif power == 1:
            var_str = variable
        else:
            var_str = ""
        
        term = f"{coeff_str}{var_str}"

        if not terms:
            terms.append(f"-{term}" if c < 0 else term)
        else:
            terms.append(f"{sign}{term}")
            
    poly_str = "".join(terms).lstrip(' +')
    return poly_str if poly_str else "0"

def format_synthetic_division_result(result):
    """
    Định dạng kết quả từ hàm chia Horner.
    """
    p_x_str = _format_poly_str(result['coeffs'])
    q_x_str = _format_poly_str(result['quotient_coeffs'])
    value = result['value']
    root = result['root']

    # P(x) = (x - c) * Q(x) + R
    result_str_latex = f"P(x) = (x - {root:g})({q_x_str}) + {value:g}"

    return {
        "status": "success",
        "method": "Sơ đồ Horner cho P(x)/(x-c)",
        "polynomial_str": p_x_str,
        "quotient_str": q_x_str,
        "value": value,
        "root": root,
        "result_str_latex": result_str_latex,
        "division_table": result['division_table'].tolist()
    }

def format_all_derivatives_result(result):
    """
    Định dạng kết quả từ hàm tính đa thức và các đạo hàm tại một điểm sử dụng Horner mở rộng.
    """
    steps = result['steps']
    values = result['values']

    formatted_steps = {}
    for step_key, step in steps.items():
        formatted_steps[step_key] = {
            "division_table": step['division_table'],
            "coeffs": step['coeffs']
        }

    return {
        "status": "success",
        "method": "Horner mở rộng cho đa thức và các đạo hàm tại một điểm",
        "steps": formatted_steps,
        "values": values
    }