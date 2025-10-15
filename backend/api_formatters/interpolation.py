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