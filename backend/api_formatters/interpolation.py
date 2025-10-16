# backend/api_formatters/interpolation.py
import numpy as np

def format_chebyshev_nodes_result(result):
    """
    Định dạng kết quả từ hàm tính mốc nội suy tối ưu Chebyshev.
    """
    if "error" in result:
        return result

    # Chuyển đổi mảng numpy thành danh sách list python thuần
    nodes_list = result.get("nodes", []).tolist()

    return {
        "status": "success",
        "method": "Mốc nội suy tối ưu Chebyshev",
        "nodes": nodes_list,
        "message": f"Đã tìm thấy {len(nodes_list)} mốc nội suy tối ưu."
    }

def _format_poly_str(coeffs, variable='x'):
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

# Thêm hàm format mới vào cuối file
def format_lagrange_interpolation_result(result):
    """
    Định dạng kết quả từ hàm nội suy Lagrange.
    """
    formatted_steps = []
    for step in result['calculation_steps']:
        formatted_steps.append({
            "i": step['i'],
            "xi": step['xi'],
            "yi": step['yi'],
            "Di_value": step['Di_value'],
            "w_over_x_minus_xi_str": _format_poly_str(step['w_over_x_minus_xi_coeffs']),
            "term_str": _format_poly_str(step['term_coeffs'])
        })

    return {
        "status": "success",
        "method": "Nội suy Lagrange",
        "polynomial_str": _format_poly_str(result['polynomial_coeffs']),
        "w_poly_str": _format_poly_str(result['w_calculation']['coeffs']),
        "calculation_steps": formatted_steps
    }