# backend/numerical_methods/interpolation/spline.py
import numpy as np
from typing import List, Dict, Any

def spline_linear(x_nodes: List[float], y_nodes: List[float]) -> Dict[str, Any]:
    """
    Tính toán hàm ghép trơn (spline) tuyến tính (cấp 1).

    Hàm S(x) được tạo thành từ các đa thức bậc 1 S_k(x) trên mỗi 
    đoạn [x_k, x_{k+1}].
    S_k(x) = a_k * x + b_k

    Dựa trên lý thuyết:
    S_k(x) là đa thức nội suy bậc 1 qua (x_k, y_k) và (x_{k+1}, y_{k+1}).
    Các hệ số được tính bằng công thức:
    a_k = (y_{k+1} - y_k) / h_k
    b_k = (y_k * x_{k+1} - y_{k+1} * x_k) / h_k
    với h_k = x_{k+1} - x_k.

    Parameters:
        x_nodes (List[float]): Danh sách các mốc x_i.
        y_nodes (List[float]): Danh sách các giá trị y_i tương ứng.

    Returns:
        Dict[str, Any]: Một từ điển chứa các đoạn spline.
    """
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)

    if len(x_nodes) != len(y_nodes):
        raise ValueError("Số lượng mốc x và giá trị y phải bằng nhau.")
    
    n = len(x_nodes)
    if n < 2:
        raise ValueError("Cần ít nhất 2 điểm để tạo spline tuyến tính.")

    # Sắp xếp các mốc theo thứ tự tăng dần của x
    sorted_indices = np.argsort(x_nodes)
    x = x_nodes[sorted_indices]
    y = y_nodes[sorted_indices]

    # Kiểm tra các mốc x có phân biệt không
    for i in range(n - 1):
        if np.isclose(x[i], x[i+1]):
            raise ValueError(f"Các mốc x phải phân biệt nhau. Mốc x={x[i]} bị lặp lại.")

    splines = []
    
    # Lặp qua n-1 đoạn
    for k in range(n - 1):
        x_k = x[k]
        y_k = y[k]
        x_k_plus_1 = x[k+1]
        y_k_plus_1 = y[k+1]
        
        h_k = x_k_plus_1 - x_k
        
        # Tính toán các hệ số a_k, b_k
        a_k = (y_k_plus_1 - y_k) / h_k
        b_k = (y_k * x_k_plus_1 - y_k_plus_1 * x_k) / h_k
        
        segment_info = {
            "k": k,
            "interval": [float(x_k), float(x_k_plus_1)],
            "coeffs": [float(a_k), float(b_k)],  # [a, b] cho S_k(x) = ax + b
        }
        splines.append(segment_info)

    return {
        "status": "success",
        "spline_type": "Linear (Cấp 1)",
        "n_points": n,
        "n_segments": n - 1,
        "splines": splines,
        "x_nodes_sorted": x.tolist(), # Thêm để tiện cho việc format
        "y_nodes_sorted": y.tolist()  # Thêm để tiện cho việc format
    }

def spline_quadratic(x_nodes: List[float], y_nodes: List[float], boundary_m1: float) -> Dict[str, Any]:
    """
    Tính toán hàm ghép trơn (spline) bậc 2 (cấp 2).

    Hàm S(x) được tạo thành từ các đa thức bậc 2 S_k(x) trên mỗi 
    đoạn [x_k, x_{k+1}] và đảm bảo S(x) liên tục cấp 1 (C^1).
    S_k(x) = a_k * x^2 + b_k * x + c_k

    Thuật toán:
    1. Đặt m_i = S'(x_i) là các ẩn. Có n ẩn (m_1, ..., m_n).
    2. Từ điều kiện S_k(x_k) = y_k và S_k(x_{k+1}) = y_{k+1}, ta xây dựng được
       hệ n-1 phương trình:
       m_k + m_{k+1} = 2 * (y_{k+1} - y_k) / h_k
    3. Cần 1 điều kiện biên (ví dụ m_1 = S'(x_1)) để giải hệ.
    4. Giải hệ để tìm tất cả các m_i.
    5. Dùng các m_i để tính hệ số a_k, b_k, c_k cho mỗi đoạn.

    Parameters:
        x_nodes (List[float]): Danh sách các mốc x_i.
        y_nodes (List[float]): Danh sách các giá trị y_i tương ứng.
        boundary_m1 (float): Giá trị điều kiện biên, S'(x_1) (đạo hàm tại mốc đầu tiên).

    Returns:
        Dict[str, Any]: Một từ điển chứa các đoạn spline.
    """
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)

    if len(x_nodes) != len(y_nodes):
        raise ValueError("Số lượng mốc x và giá trị y phải bằng nhau.")
    
    n = len(x_nodes)
    if n < 2:
        raise ValueError("Cần ít nhất 2 điểm để tạo spline.")

    # Sắp xếp các mốc theo thứ tự tăng dần của x
    sorted_indices = np.argsort(x_nodes)
    x = x_nodes[sorted_indices]
    y = y_nodes[sorted_indices]

    h = np.zeros(n - 1)
    # Kiểm tra các mốc x có phân biệt không và tính h_k
    for i in range(n - 1):
        if np.isclose(x[i], x[i+1]):
            raise ValueError(f"Các mốc x phải phân biệt nhau. Mốc x={x[i]} bị lặp lại.")
        h[i] = x[i+1] - x[i]
        
    # Khởi tạo mảng chứa các giá trị đạo hàm m_i = S'(x_i)
    m = np.zeros(n)
    m[0] = boundary_m1  # Áp dụng điều kiện biên
    
    # *** THÊM MỚI: Lưu trữ gamma_k để hiển thị ***
    gammas = np.zeros(n - 1)

    # Giải hệ n-1 phương trình để tìm m_2, ..., m_n
    # m_k + m_{k+1} = 2 * (y_{k+1} - y_k) / h_k => m_{k+1} = ... - m_k
    for k in range(n - 1):
        gamma_k = 2 * (y[k+1] - y[k]) / h[k]
        gammas[k] = gamma_k # *** THÊM MỚI ***
        m[k+1] = gamma_k - m[k]

    # Tính toán các hệ số a_k, b_k, c_k cho từng đoạn spline
    splines = []
    for k in range(n - 1):
        x_k = x[k]
        y_k = y[k]
        x_k_plus_1 = x[k+1]
        m_k = m[k]
        m_k_plus_1 = m[k+1]
        h_k = h[k]
        
        # S_k(x) = a_k * x^2 + b_k * x + c_k
        #
        a_k = (m_k_plus_1 - m_k) / (2 * h_k)
        b_k = (m_k * x_k_plus_1 - m_k_plus_1 * x_k) / h_k
        
        # c_k tính từ S_k(x_k) = y_k
        theta_k = y_k + (m_k * h_k) / 2
        c_k = ((-m_k * x_k_plus_1**2) + (m_k_plus_1 * x_k**2)) / (2 * h_k) + theta_k
        
        segment_info = {
            "k": k,
            "interval": [float(x_k), float(x_k_plus_1)],
            "coeffs": [float(a_k), float(b_k), float(c_k)],  # [a, b, c]
        }
        splines.append(segment_info)

    return {
        "status": "success",
        "spline_type": "Quadratic (Cấp 2)",
        "n_points": n,
        "n_segments": n - 1,
        "m_values": m.tolist(),  # Trả về các giá trị S'(x_i) đã tính được
        "gammas": gammas.tolist(), # *** THÊM MỚI ***
        "splines": splines,
        "x_nodes_sorted": x.tolist(),
        "y_nodes_sorted": y.tolist()
    }

def spline_cubic(x_nodes: List[float], y_nodes: List[float], 
                 boundary_alpha_start: float, boundary_alpha_end: float) -> Dict[str, Any]:
    """
    Tính toán hàm ghép trơn (spline) bậc 3 (cấp 3).
    Sử dụng điều kiện biên S''(x_0) và S''(x_{n-1}) (ví dụ: 0 cho Spline Tự nhiên).
    
    Thuật toán:
    1. Đặt alpha_i = S''(x_i) là các ẩn.
    2. Xây dựng hệ n-2 phương trình tuyến tính cho n-2 ẩn (alpha_1, ..., alpha_{n-2})
       dựa trên điều kiện S'(x) liên tục.
       (h_{k-1}/6)alpha_{k-1} + ((h_{k-1}+h_k)/3)alpha_k + (h_k/6)alpha_{k+1} = gamma_k
       với gamma_k = (y_{k+1}-y_k)/h_k - (y_k-y_{k-1})/h_{k-1} 
       (Lưu ý: Index k ở đây tương ứng k+1 trong slide)
    3. Áp dụng điều kiện biên alpha_0 = boundary_alpha_start và alpha_{n-1} = boundary_alpha_end.
    4. Giải hệ (n-2)x(n-2) để tìm alpha_1, ..., alpha_{n-2}.
    5. Tính các hệ số đa thức S_k(x) = a_k(x-x_k)^3 + b_k(x-x_k)^2 + c_k(x-x_k) + d_k.

    Parameters:
        x_nodes (List[float]): Danh sách các mốc x_i (n điểm).
        y_nodes (List[float]): Danh sách các giá trị y_i (n điểm).
        boundary_alpha_start (float): Giá trị S''(x_0). (0 cho spline tự nhiên).
        boundary_alpha_end (float): Giá trị S''(x_{n-1}). (0 cho spline tự nhiên).

    Returns:
        Dict[str, Any]: Một từ điển chứa các đoạn spline.
    """
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)

    if len(x_nodes) != len(y_nodes):
        raise ValueError("Số lượng mốc x và giá trị y phải bằng nhau.")
    
    n = len(x_nodes)
    if n < 3:
        raise ValueError("Cần ít nhất 3 điểm (2 đoạn) để tạo spline bậc 3.")

    # Sắp xếp và tính h_k
    sorted_indices = np.argsort(x_nodes)
    x = x_nodes[sorted_indices]
    y = y_nodes[sorted_indices]

    h = np.zeros(n - 1)
    for i in range(n - 1):
        if np.isclose(x[i], x[i+1]):
            raise ValueError(f"Các mốc x phải phân biệt nhau. Mốc x={x[i]} bị lặp lại.")
        h[i] = x[i+1] - x[i]
        
    # Khởi tạo mảng alpha (S''(x_i))
    alpha = np.zeros(n)
    alpha[0] = boundary_alpha_start
    alpha[-1] = boundary_alpha_end
    
    # --- Xây dựng hệ (n-2)x(n-2) cho các alpha nội bộ (alpha_1, ..., alpha_{n-2}) ---
    
    # 1. Tạo ma trận M (n-2, n-2)
    M = np.zeros((n-2, n-2))
    
    # Đường chéo chính
    diag_main = (h[:-1] + h[1:]) / 3.0
    np.fill_diagonal(M, diag_main)
    
    # Đường chéo phụ trên
    diag_upper = h[1:-1] / 6.0
    # === SỬA LỖI ===
    # np.fill_diagonal(M[0, 1:], diag_upper) # Lỗi: M[0, 1:] là 1D
    np.fill_diagonal(M[0:, 1:], diag_upper) # Sửa: M[0:, 1:] là 2D
    
    # Đường chéo phụ dưới
    diag_lower = h[1:-1] / 6.0
    # === SỬA LỖI ===
    # np.fill_diagonal(M[1, 0:], diag_lower) # Lỗi: M[1, 0:] là 1D
    np.fill_diagonal(M[1:, 0:], diag_lower) # Sửa: M[1:, 0:] là 2D
    
    # 2. Tạo vector vế phải R = gamma
    R = (y[2:] - y[1:-1]) / h[1:] - (y[1:-1] - y[:-2]) / h[:-1]
    
    # 3. Điều chỉnh vế phải R theo điều kiện biên
    # Điều chỉnh cho alpha[0]
    if n > 2: # Chỉ thực hiện nếu có ít nhất 1 phương trình
        R[0] -= (h[0] / 6.0) * alpha[0]
    # Điều chỉnh cho alpha[n-1]
    if n > 3: # Chỉ thực hiện nếu có ít nhất 2 phương trình (để R[-1] tồn tại và khác R[0])
        R[-1] -= (h[-2] / 6.0) * alpha[-1] # Sửa h[-1] thành h[-2] cho đúng (h cuối là h[n-2])

    # 4. Giải hệ M * internal_alphas = R
    try:
        if n-2 > 0: # Chỉ giải hệ nếu có các ẩn alpha bên trong
            internal_alphas = np.linalg.solve(M, R)
            alpha[1:-1] = internal_alphas
    except np.linalg.LinAlgError:
        raise ValueError("Hệ phương trình suy biến. Không thể giải tìm các hệ số alpha.")
        
    
    # --- Tính toán các hệ số spline ---
    # S_k(x) = a_k(x-x_k)^3 + b_k(x-x_k)^2 + c_k(x-x_k) + d_k
    splines = []
    for k in range(n - 1): # Lặp qua n-1 đoạn
        x_k = x[k]
        y_k = y[k]
        h_k = h[k]
        alpha_k = alpha[k]
        alpha_k_plus_1 = alpha[k+1]
        
        # S_k(t) = a_k*t^3 + b_k*t^2 + c_k*t + d_k, với t = (x - x_k)
        # S_k(x_k) = d_k = y_k
        d_k = y_k
        
        # S_k''(x_k) = 2*b_k = alpha_k
        b_k = alpha_k / 2.0
        
        # S_k''(x_{k+1}) = 6*a_k*h_k + 2*b_k = alpha_{k+1}
        a_k = (alpha_k_plus_1 - alpha_k) / (6 * h_k)
        
        # S_k(x_{k+1}) = a_k*h_k^3 + b_k*h_k^2 + c_k*h_k + d_k = y_{k+1}
        c_k = (y[k+1] - y_k) / h_k - (h_k * (2*alpha_k + alpha_k_plus_1)) / 6.0
        
        segment_info = {
            "k": k,
            "interval": [float(x_k), float(x[k+1])],
            "shift_point": float(x_k), # Điểm x_k dùng để dịch (shift)
            "coeffs": [float(a_k), float(b_k), float(c_k), float(d_k)],
        }
        splines.append(segment_info)
        
    return {
        "status": "success",
        "spline_type": "Cubic (Cấp 3)",
        "n_points": n,
        "n_segments": n - 1,
        "alpha_values": alpha.tolist(), # Trả về các giá trị S''(x_i)
        "splines": splines,
        "x_nodes_sorted": x.tolist(),
        "y_nodes_sorted": y.tolist(),
        # *** THÊM MỚI: Trả về hệ phương trình đã giải ***
        "intermediate_system": {
            "M": M,
            "R": R.reshape(-1, 1) # Đảm bảo R là vector cột
        }
    }