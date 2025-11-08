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

def format_divided_difference_result(result):
    """
    Định dạng kết quả từ hàm tính bảng tỷ sai phân.
    """
    if "error" in result:
        return result

    return {
        "status": "success",
        "method": "Tỷ sai phân",
        "divided_difference_table": result.get("divided_difference_table", []),
        "message": f"Đã tính xong bảng tỷ sai phân cho {len(result.get('divided_difference_table', []))} điểm."
    }

def format_finite_difference_result(result):
    """
    Định dạng kết quả từ hàm tính bảng sai phân.
    """
    if "error" in result:
        return result

    return {
        "status": "success",
        "method": "Sai phân",
        "finite_difference_table": result.get("finite_difference_table", []),
        "message": f"Đã tính xong bảng sai phân cho {len(result.get('finite_difference_table', []))} điểm."
    }

def format_newton_interpolation_result(result):
    """
    Định dạng kết quả từ hàm nội suy Newton mốc cách đều.
    """
    if "error" in result:
        return result

    def format_interpolation_details(details):
        # Helper to format each term of the polynomial sum
        terms_str = []
        for i in range(len(details["coeffs_scaled"])):
            coeff = details["coeffs_scaled"][i]
            w_poly = details["w_polynomials_t"][i]
            
            if abs(coeff) < 1e-12:
                continue

            w_poly_str = _format_poly_str(w_poly, variable='t')
            coeff_str = f"{abs(coeff):g}"
            
            term = ""
            if not terms_str:
                term = f"- {coeff_str}" if coeff < 0 else f"{coeff_str}"
            else:
                term = f" - {coeff_str}" if coeff < 0 else f" + {coeff_str}"

            if w_poly_str and w_poly_str != "1":
                 term += f"({w_poly_str})"
            
            terms_str.append(term)
        
        poly_sum_str = " ".join(terms_str).lstrip(" +")

        return {
            "start_node": details["start_node"],
            "diffs": [float(d) for d in details["diffs"]],
            "coeffs_scaled": [float(c) for c in details["coeffs_scaled"]],
            "w_polynomials_t": [[float(c) for c in p] for p in details["w_polynomials_t"]],
            "polynomial_sum_str_t": poly_sum_str or "0",
            "polynomial_str_t": _format_poly_str(details["polynomial_coeffs_t"], variable='t'),
            "polynomial_coeffs_t": details["polynomial_coeffs_t"],
            "polynomial_str_x": _format_poly_str(details["polynomial_coeffs_x"], variable='x'),
            "polynomial_coeffs_x": details["polynomial_coeffs_x"]
        }

    return {
        "status": "success",
        "method": "Nội suy Newton mốc cách đều",
        "message": "Tính toán đa thức nội suy Newton thành công.",
        "finite_difference_table": result["finite_difference_table"],
        "h": result["h"],
        "forward_interpolation": format_interpolation_details(result["forward_interpolation"]),
        "backward_interpolation": format_interpolation_details(result["backward_interpolation"])
    }

def format_newton_divided_interpolation_result(result):
    """
    Định dạng kết quả từ hàm nội suy Newton mốc bất kỳ (dùng tỷ sai phân).
    """
    if "error" in result:
        return result

    def format_interpolation_details(details):
        # Helper to format each term of the polynomial sum
        terms_str = []
        for i in range(len(details["diffs"])):
            coeff = details["diffs"][i] # Hệ số là tỷ sai phân luôn
            w_poly = details["w_polynomials_t"][i] # Đây thực chất là w_polynomials_x

            if abs(coeff) < 1e-12:
                continue

            w_poly_str = _format_poly_str(w_poly, variable='x')
            coeff_str = f"{abs(coeff):g}"

            term = ""
            if not terms_str:
                term = f"- {coeff_str}" if coeff < 0 else f"{coeff_str}"
            else:
                term = f" - {coeff_str}" if coeff < 0 else f" + {coeff_str}"

            if w_poly_str and w_poly_str != "1":
                 term += f"({w_poly_str})"

            terms_str.append(term)

        poly_sum_str = " ".join(terms_str).lstrip(" +")

        return {
            "start_node": details["start_node"],
            "diffs": [float(d) for d in details["diffs"]],
            # "coeffs_scaled" không cần thiết vì dùng trực tiếp diffs
            "w_polynomials_x": [[float(c) for c in p] for p in details["w_polynomials_t"]], # Đổi tên cho rõ
            "polynomial_sum_str_x": poly_sum_str or "0",
            "polynomial_str_x": _format_poly_str(details["polynomial_coeffs"], variable='x'),
            "polynomial_coeffs_x": details["polynomial_coeffs"]
        }

    return {
        "status": "success",
        "method": "Nội suy Newton mốc bất kỳ (Tỷ sai phân)",
        "message": "Tính toán đa thức nội suy Newton thành công.",
        "divided_difference_table": result["divided_difference_table"],
        "x_nodes_sorted": result["x_nodes_sorted"],
        "y_nodes_sorted": result["y_nodes_sorted"],
        "forward_interpolation": format_interpolation_details(result["forward_interpolation"]),
        "backward_interpolation": format_interpolation_details(result["backward_interpolation"])
    }

def format_central_gauss_i_result(result):
    """
    Định dạng kết quả từ hàm nội suy trung tâm Gauss I.
    """
    if "error" in result:
        return result

    finite_difference_table = [[float(v) for v in row] for row in result.get("finite_difference_table", [])]
    central_finite_diffs = [float(v) for v in result.get("central_finite_diffs", [])]
    c_coeffs = [float(v) for v in result.get("c_coeffs", [])]

    w_table_coeffs_formatted = []
    for coeffs_list in result.get("w_table", []): 
        w_table_coeffs_formatted.append([float(c) for c in coeffs_list])

    polynomial_coeffs_t = [float(v) for v in result.get("polynomial_coeffs_t", [])]
    polynomial_coeffs_x = [float(v) for v in result.get("polynomial_coeffs_x", [])]

    return {
        "status": "success",
        "method": "Nội suy trung tâm Gauss I",
        "message": f"Tính toán đa thức nội suy Gauss I thành công cho {len(finite_difference_table)} điểm.",
        "start_node": float(result.get("start_node")),
        "h": float(result.get("h")),
        "t_nodes": [float(t) for t in result.get("t_nodes", [])], 
        "finite_difference_table": finite_difference_table,
        "central_finite_diffs": central_finite_diffs,
        "c_coeffs": c_coeffs,
        "w_table_coeffs": w_table_coeffs_formatted, 
        "polynomial_coeffs_t": polynomial_coeffs_t,
        "polynomial_str_t": _format_poly_str(polynomial_coeffs_t, variable='t'),
        "polynomial_coeffs_x": polynomial_coeffs_x,
        "polynomial_str_x": _format_poly_str(polynomial_coeffs_x, variable='x')
    }

def format_central_gauss_ii_result(result):
    """
    Định dạng kết quả từ hàm nội suy trung tâm Gauss II.
    """
    if "error" in result:
        return result

    # Chuyển đổi tất cả các giá trị numpy/float sang kiểu Python gốc
    finite_difference_table = [[float(v) for v in row] for row in result.get("finite_difference_table", [])]
    central_finite_diffs = [float(v) for v in result.get("central_finite_diffs", [])]
    c_coeffs = [float(v) for v in result.get("c_coeffs", [])]
    
    w_table_coeffs_formatted = []
    for coeffs_list in result.get("w_table", []): 
        w_table_coeffs_formatted.append([float(c) for c in coeffs_list])

    polynomial_coeffs_t = [float(v) for v in result.get("polynomial_coeffs_t", [])]
    polynomial_coeffs_x = [float(v) for v in result.get("polynomial_coeffs_x", [])]

    return {
        "status": "success",
        "method": "Nội suy trung tâm Gauss II",
        "message": f"Tính toán đa thức nội suy Gauss II thành công cho {len(finite_difference_table)} điểm.",
        "start_node": float(result.get("start_node")),
        "h": float(result.get("h")),
        "t_nodes": [float(t) for t in result.get("t_nodes", [])], 
        "finite_difference_table": finite_difference_table,
        "central_finite_diffs": central_finite_diffs,
        "c_coeffs": c_coeffs,
        "w_table_coeffs": w_table_coeffs_formatted, 
        "polynomial_coeffs_t": polynomial_coeffs_t,
        "polynomial_str_t": _format_poly_str(polynomial_coeffs_t, variable='t'),
        "polynomial_coeffs_x": polynomial_coeffs_x,
        "polynomial_str_x": _format_poly_str(polynomial_coeffs_x, variable='x')
    }

def format_stirling_interpolation_result(result):
    """
    Định dạng kết quả từ hàm nội suy trung tâm Stirling.
    """
    if "error" in result:
        return result

    finite_difference_table = [[float(v) for v in row] for row in result.get("finite_difference_table", [])]
    central_finite_diffs = [float(v) for v in result.get("central_finite_diffs", [])]
    c_coeffs = [float(v) for v in result.get("c_coeffs", [])]
    
    w_table_coeffs_formatted = []
    for coeffs_list in result.get("w_table", []): 
        w_table_coeffs_formatted.append([float(c) for c in coeffs_list])

    polynomial_coeffs_t = [float(v) for v in result.get("polynomial_coeffs_t", [])]
    polynomial_coeffs_x = [float(v) for v in result.get("polynomial_coeffs_x", [])]

    return {
        "status": "success",
        "method": "Nội suy Stirling",
        "message": f"Tính toán đa thức nội suy Stirling thành công cho {len(finite_difference_table)} điểm.",
        "start_node": float(result.get("start_node")),
        "h": float(result.get("h")),
        "t_nodes": [float(t) for t in result.get("t_nodes", [])], 
        "finite_difference_table": finite_difference_table,
        "central_finite_diffs": central_finite_diffs,
        "c_coeffs": c_coeffs,
        "w_table_coeffs": w_table_coeffs_formatted,
        "polynomial_coeffs_t": polynomial_coeffs_t,
        "polynomial_str_t": _format_poly_str(polynomial_coeffs_t, variable='t'),
        "polynomial_coeffs_x": polynomial_coeffs_x,
        "polynomial_str_x": _format_poly_str(polynomial_coeffs_x, variable='x'),
        # Thêm các trường
        "central_finite_diffs_i": [float(v) for v in result.get("central_finite_diffs_i", [])],
        "central_finite_diffs_ii": [float(v) for v in result.get("central_finite_diffs_ii", [])],
        "stirlin_polynomial_t_even": [float(v) for v in result.get("stirlin_polynomial_t_even", [])],
        "stirlin_polynomial_t_odd": [float(v) for v in result.get("stirlin_polynomial_t_odd", [])],
    }

def format_bessel_interpolation_result(result):
    """
    Định dạng kết quả từ hàm nội suy trung tâm Bessel.
    """
    if "error" in result:
        return result

    finite_difference_table = [[float(v) for v in row] for row in result.get("finite_difference_table", [])]
    central_finite_diffs = [float(v) for v in result.get("central_finite_diffs", [])]
    c_coeffs = [float(v) for v in result.get("c_coeffs", [])]
    
    w_table_coeffs_formatted = []
    for coeffs_list in result.get("w_table", []): 
        w_table_coeffs_formatted.append([float(c) for c in coeffs_list])

    polynomial_coeffs_u = [float(v) for v in result.get("bessel_polynomial_coeffs_u", [])]
    polynomial_coeffs_t = [float(v) for v in result.get("bessel_polynomial_coeffs_t", [])]
    polynomial_coeffs_x = [float(v) for v in result.get("bessel_polynomial_coeffs_x", [])]

    return {
        "status": "success",
        "method": "Nội suy Bessel",
        "message": f"Tính toán đa thức nội suy Bessel thành công cho {len(finite_difference_table)} điểm.",
        "start_node": float(result.get("start_node")),
        "h": float(result.get("h")),
        "t_nodes": [float(t) for t in result.get("t_nodes", [])],
        "u_nodes": [float(u) for u in result.get("u_nodes", [])],
        "finite_difference_table": finite_difference_table,
        "central_finite_diffs": central_finite_diffs,
        "c_coeffs": c_coeffs,
        "w_table_coeffs": w_table_coeffs_formatted,
        "polynomial_coeffs_u": polynomial_coeffs_u,
        "polynomial_str_u": _format_poly_str(polynomial_coeffs_u, variable='u'),
        "polynomial_coeffs_t": polynomial_coeffs_t,
        "polynomial_str_t": _format_poly_str(polynomial_coeffs_t, variable='t'),
        "polynomial_coeffs_x": polynomial_coeffs_x,
        "polynomial_str_x": _format_poly_str(polynomial_coeffs_x, variable='x'),
        # Thêm các trường
        "central_finite_diffs_i": [float(v) for v in result.get("central_finite_diffs_i", [])],
        "central_finite_diffs_ii": [float(v) for v in result.get("central_finite_diffs_ii", [])],
        "bessel_polynomial_u_even": [float(v) for v in result.get("bessel_polynomial_u_even", [])],
        "bessel_polynomial_u_odd": [float(v) for v in result.get("bessel_polynomial_u_odd", [])],
    }

def format_spline_result(result):
    """
    Định dạng kết quả từ các hàm spline.
    """
    if result.get("status") != "success":
        return result

    # Chuyển đổi tất cả các giá trị numpy/float sang kiểu Python gốc
    splines_formatted = []
    for segment in result.get("splines", []):
        splines_formatted.append({
            "k": segment["k"],
            "interval": [float(v) for v in segment["interval"]],
            "coeffs": [float(v) for v in segment["coeffs"]],
            # Thêm shift_point nếu có (cho spline bậc 3)
            "shift_point": float(segment["shift_point"]) if "shift_point" in segment else None
        })

    formatted = {
        "status": "success",
        "method": f"Hàm ghép trơn {result['spline_type']}",
        "message": f"Tính toán {result['n_segments']} đoạn spline thành công.",
        "spline_type": result['spline_type'],
        "x_nodes_sorted": [float(v) for v in result.get("x_nodes_sorted", [])],
        "y_nodes_sorted": [float(v) for v in result.get("y_nodes_sorted", [])],
        "splines": splines_formatted
    }

    if "m_values" in result:
        formatted["m_values"] = [float(v) for v in result["m_values"]]
    # *** THÊM MỚI: Chuyển đổi gammas ***
    if "gammas" in result:
        formatted["gammas"] = [float(g) for g in result["gammas"]]
        
    if "alpha_values" in result:
        formatted["alpha_values"] = [float(v) for v in result["alpha_values"]]
    
    # *** THÊM MỚI: Chuyển đổi hệ phương trình M, R cho cubic ***
    if "intermediate_system" in result:
        formatted["intermediate_system"] = {
            "M": result["intermediate_system"]["M"].tolist(),
            "R": result["intermediate_system"]["R"].tolist()
        }

    return formatted

def format_lsq_result(result):
    """
    Định dạng kết quả từ hàm bình phương tối thiểu.
    """
    if result.get("status") != "success":
        return result
    
    # Hàm g(x) đã được định dạng LaTeX từ backend
    # Các ma trận trung gian cũng đã được chuyển đổi sang list
    return result