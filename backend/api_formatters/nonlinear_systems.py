# backend/api_formatters/nonlinear_systems.py

def format_nonlinear_system_result(method_name, result):
    """
    Định dạng kết quả từ các phương pháp giải hệ phi tuyến.
    """
    if result.get('status') != 'success':
        return {"error": result.get('error', 'Lỗi không xác định')}

    # Dữ liệu trả về sẽ thay đổi tùy theo phương pháp,
    # chúng ta chỉ cần thêm các key nếu chúng tồn tại trong `result`
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
        
    return response