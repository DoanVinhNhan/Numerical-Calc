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
        "quotient_coeffs": result['quotient_coeffs'].tolist(),
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
        "product_coeffs": result['coeffs'],
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
        "final_poly_coeffs": final_coeffs,
        "steps": formatted_steps
    }

def format_change_variables_result(result):
    original_poly_str = _format_poly_str(result['original_coeffs'], variable='x')
    new_poly_str = _format_poly_str(result['variables_coeffs'], variable='t')
    a = result['a']
    b = result['b']
    x0 = -b / a
    n = len(result['original_coeffs']) - 1

    formatted_steps = []
    # --- Lấy các hệ số d_k (remainder_dk) từ các bước ---
    taylor_coeffs_dk = []
    for step_data in result['steps']:
        division_table = np.array(step_data['division_table']).tolist()
        quotient_coeffs = np.array(step_data['quotient_coeffs']).tolist()
        q_x_str = _format_poly_str(quotient_coeffs)
        remainder = step_data['remainder_dk']
        taylor_coeffs_dk.append(remainder) # Lưu lại d_k

        formatted_steps.append({
            "step_index": step_data['step_index'],
            "division_table": division_table,
            "quotient_str": q_x_str,
            "remainder_dk": remainder
        })

    # --- Thêm phần giải thích công thức ---
    taylor_expansion_x_str = f"P(x) = \\sum_{{k=0}}^{{{n}}} d_k (x - x_0)^k"
    taylor_expansion_t_str = f"Q(t) = P(x)|_{{x=\\frac{{t-b}}{{a}}}} = \\sum_{{k=0}}^{{{n}}} d_k \\left(\\frac{{t}}{{a}}\\right)^k = \\sum_{{k=0}}^{{{n}}} \\left(\\frac{{d_k}}{{a^k}}\\right) t^k"

    # --- Tính toán và giải thích các hệ số của Q(t) ---
    q_coeffs_explanation = []
    a_prime = 1.0 / a
    # Tính toán các hệ số q_k = d_k / a^k (theo thứ tự tăng dần của k)
    coeffs_q_ascending = [dk * (a_prime**k) for k, dk in enumerate(taylor_coeffs_dk)]

    for k in range(n + 1):
        q_coeff_value = coeffs_q_ascending[k]
        dk_value = taylor_coeffs_dk[k]
        q_coeffs_explanation.append({
            "k": k,
            "dk_value": dk_value,
            "formula": f"q_{k} = \\frac{{d_{k}}}{{a^{k}}} = \\frac{{{dk_value:g}}}{{{a:g}^{k}}}",
            "value": q_coeff_value
        })

    return {
        "status": "success",
        "method": "Đổi biến đa thức",
        "original_poly_str": original_poly_str,
        "new_poly_str": new_poly_str,
        "new_poly_coeffs": result['variables_coeffs'],
        "a": a,
        "b": b,
        "root": x0,
        "steps": formatted_steps,
        "taylor_explanation": { # Thêm mục giải thích mới
            "taylor_coeffs_dk": taylor_coeffs_dk,
            "taylor_expansion_x_str": taylor_expansion_x_str,
            "taylor_expansion_t_str": taylor_expansion_t_str,
            "q_coeffs_explanation": q_coeffs_explanation
        }
    }