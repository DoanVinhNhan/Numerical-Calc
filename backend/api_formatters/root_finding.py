# backend/api_formatters/root_finding.py
import numpy as np

def format_root_finding_result(method_name, result, mode=None, stop_condition=None):
    """
    Định dạng kết quả từ các phương pháp tìm nghiệm.
    """
    if not result:
        return {"error": "Không có kết quả để định dạng."}

    # Xác định tên cột sai số dựa trên phương pháp và điều kiện dừng
    error_col_name = "error" # Mặc định
    if "Chia đôi" in method_name:
        error_col_name = "|c_n - c_{n-1}|"
    elif "Dây cung" in method_name:
        if mode == 'absolute_error':
            error_col_name = "|f(x_n)|/m_1" if stop_condition == 'f_xn' else "(M_1-m_1)|x_n-x_{n-1}|/m_1"
        elif mode == 'relative_error':
            error_col_name = "|f(x_n)|/(m_1|x_n|)" if stop_condition == 'f_xn' else "(M_1-m_1)|x_n-x_{n-1}|/(m_1|x_n|)"
    elif "Newton" in method_name:
        if mode == 'absolute_error':
            error_col_name = "|f(x_{n+1})|/m_1" if stop_condition == 'f_xn' else "(M_2/2m_1)|x_{n+1}-x_n|^2"
        elif mode == 'relative_error':
            error_col_name = "|f(x_{n+1})|/(m_1|x_{n+1}|)" if stop_condition == 'f_xn' else "(M_2/2m_1)|x_{n+1}-x_n|^2/|x_{n+1}|"
    elif "Lặp đơn" in method_name:
        error_col_name = "(q/(1-q))|x_{k+1}-x_k|"

    # Chuyển đổi các giá trị numpy thành kiểu dữ liệu Python gốc
    for step in result['steps']:
        for key, value in step.items():
            if isinstance(value, np.generic):
                step[key] = value.item()

    return {
        "method": method_name,
        "status": "success",
        "message": f"Tìm thấy nghiệm thành công sau {result['iterations']} lần lặp.",
        "solution": result['solution'],
        "steps": result['steps'],
        "error_col_name": error_col_name, # Gửi tên cột cho frontend
        "extra_info": { # Gửi thêm thông tin cho Secant
            "m1": result.get("m1"),
            "M1": result.get("M1"),
            "d": result.get("d"),
            "x0": result.get("x0")
        }
    }