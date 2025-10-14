# backend/api_formatters/root_finding.py
import numpy as np

def format_root_finding_result(method_name, result):
    """
    Định dạng kết quả từ các phương pháp tìm nghiệm.
    """
    if not result:
        return {"error": "Không có kết quả để định dạng."}

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
        "steps": result['steps']
    }