# backend/api_formatters/nonlinear_systems.py

def format_nonlinear_system_result(method_name, result, stop_option=None, stop_value=None):
    """
    Định dạng kết quả từ các phương pháp giải hệ phi tuyến.
    """
    if result.get('status') != 'success':
        return {"error": result.get('error', 'Lỗi không xác định')}

    response = {
        "method": method_name,
        "status": "success",
        "message": result.get('message'),
        "solution": result.get('solution'),
        "iterations": result.get('iterations'),
        "steps": result.get('steps')
    }
    
    # Thêm các trường đặc trưng cho từng phương pháp
    if 'jacobian_matrix_latex' in result:
        response['jacobian_matrix_latex'] = result['jacobian_matrix_latex']
        
    if 'J0_inv_matrix' in result:
        response['J0_inv_matrix'] = result['J0_inv_matrix']

    # Bổ sung logic cho Lặp Đơn
    if method_name == "Phương pháp Lặp đơn":
        norm_used = result.get("norm_used_for_K")
        norm_symbol = '\\infty' if norm_used == 'infinity' else '1'
        
        # Tạo chuỗi công thức điều kiện dừng
        formula = ""
        k_factor = result.get("contraction_factor_K")

        # Chỉ thêm hệ số co nếu nó hợp lệ và nhỏ hơn 1
        error_prefix = ""
        if k_factor is not None and k_factor < 1:
            error_prefix = f"\\frac{{K}}{{1-K}} "

        if stop_option == 'absolute_error':
            # Công thức sai số tuyệt đối hậu nghiệm
            formula = f"{error_prefix}||X^{{(k)}} - X^{{(k-1)}}||_{{{norm_symbol}}} < {stop_value}"
        elif stop_option == 'relative_error':
            # Công thức sai số tương đối hậu nghiệm
            formula = f"\\frac{{{error_prefix}||X^{{(k)}} - X^{{(k-1)}}||_{{{norm_symbol}}}}}{{||X^{{(k)}}||_{{{norm_symbol}}}}} < {stop_value}"
            
        convergence_info = {
            "J_max_vals": result.get("J_max_vals"),
            "max_row_sum": result.get("max_row_sum"),
            "max_col_sum": result.get("max_col_sum"),
            "contraction_factor_K": result.get("contraction_factor_K"),
            "norm_used_for_K": result.get("norm_used_for_K"),
            "stopping_condition_formula": formula  # Thêm công thức vào response
        }
        response['convergence_info'] = convergence_info
        
    return response