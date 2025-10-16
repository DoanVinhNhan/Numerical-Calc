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
    p_x_str = _format_poly_str(result['coeffs'])
    root = result['root']
    steps = result['steps']
    values = result['values']
    derivatives = result['derivatives']

    formatted_steps = []
    # Sắp xếp các bước theo đúng thứ tự step_0, step_1,...
    for i in range(len(steps)):
        step_key = f"step_{i}"
        if step_key in steps:
            step_data = steps[step_key]
            # Chuyển đổi ndarray thành list nếu cần
            division_table = np.array(step_data['division_table']).tolist()
            quotient_coeffs = np.array(step_data['coeffs']).tolist()
            
            # Tạo đa thức thương Q_i(x)
            q_x_str = _format_poly_str(quotient_coeffs)
            
            formatted_steps.append({
                "step_index": i,
                "division_table": division_table,
                "quotient_str": q_x_str,
                "remainder": values[i]
            })

    # Tạo chuỗi kết quả Taylor
    taylor_terms = []
    for i, val in enumerate(derivatives):
        term = f"\\frac{{{val:g}}}{{{i}!}}(x - {root:g})^{{{i}}}"
        taylor_terms.append(term)
    taylor_str = " + ".join(taylor_terms)


    return {
        "status": "success",
        "method": "Horner mở rộng - Tính P(c) và các đạo hàm",
        "polynomial_str": p_x_str,
        "root": root,
        "steps": formatted_steps,
        "values": values,
        "derivatives": derivatives,
        "taylor_str": taylor_str
    }

def format_reverse_horner_result(result):
    """
    Định dạng kết quả từ hàm nhân Horner.
    """
    p_x_str = _format_poly_str(result['original_coeffs'])
    q_x_str = _format_poly_str(result['coeffs'])
    root = result['root']

    # Q(x) = P(x) * (x - c)
    result_str_latex = f"({p_x_str}) \\cdot (x - {root:g})={q_x_str}"

    return {
        "status": "success",
        "method": "Sơ đồ Horner cho P(x) * (x-c)",
        "polynomial_str": p_x_str,
        "product_str": q_x_str,
        "root": root,
        "result_str_latex": result_str_latex,
        "reverse_table": result['reverse_table']
    }

def format_w_function_result(result):
    """
    Định dạng kết quả từ hàm tính Omega function.
    """
    steps = result['steps']
    final_coeffs = result['final_coeffs']
    roots = result['roots']

    formatted_steps = []
    for step in steps:
        w_k_str = _format_poly_str(step['w_k_coeffs'])
        w_k_plus_1_str = _format_poly_str(step['w_k_plus_1_coeffs'])
        
        formatted_steps.append({
            "step_index": step['step_index'],
            "w_k_str": w_k_str,
            "root": step['root'],
            "reverse_table": step['reverse_table'],
            "w_k_plus_1_str": w_k_plus_1_str
        })
        
    final_poly_str = _format_poly_str(final_coeffs)
    
    # Tạo chuỗi LaTeX cho công thức tổng quát
    factors = [f"(x - {r:g})" for r in roots]
    w_n_plus_1_latex = f"w_{{{len(roots)}}}(x) = \\prod_{{i=0}}^{{{len(roots)-1}}} (x - x_i) = {' '.join(factors)}"

    return {
        "status": "success",
        "method": "Tính Đa thức Omega",
        "w_n_plus_1_latex": w_n_plus_1_latex,
        "final_poly_str": final_poly_str,
        "steps": formatted_steps
    }