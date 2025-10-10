# backend/numerical_methods/linear_algebra/inverse/bordering.py
import numpy as np
from backend.utils.helpers import zero_small

def bordering_inverse(A, tol=1e-15):
    """
    Tính ma trận nghịch đảo bằng phương pháp viền quanh.
    """
    if A.shape[0] != A.shape[1]:
        raise ValueError("Ma trận phải là ma trận vuông.")
    
    n = A.shape[0]
    steps = []
    
    # Bước 1: Khởi tạo với ma trận con cấp 1
    if abs(A[0, 0]) < tol:
        raise ValueError("Phần tử A[0,0] bằng 0, không thể bắt đầu phương pháp viền quanh.")
    
    inv_Ak = np.array([[1.0 / A[0, 0]]])
    steps.append({
        "k": 1,
        "A_k": A[0,0],
        "inv_A_k": inv_Ak
    })

    # Bước 2: Lặp từ cấp 2 đến n
    for k in range(1, n):
        # Tách các khối từ ma trận A cấp k+1
        u_k = A[:k, k].reshape(-1, 1)      # Cột viền
        v_k_T = A[k, :k].reshape(1, -1)   # Hàng viền
        a_kk = A[k, k]
        
        # Tính các thành phần trung gian
        inv_Ak_u_k = inv_Ak @ u_k
        v_k_T_inv_Ak = v_k_T @ inv_Ak
        
        theta_k = a_kk - (v_k_T @ inv_Ak_u_k)[0, 0]
        if abs(theta_k) < tol:
            raise ValueError(f"Ma trận suy biến tại bước k={k+1} (theta ≈ 0).")

        # Tính các khối của ma trận nghịch đảo mới
        B11 = inv_Ak + (inv_Ak_u_k @ v_k_T_inv_Ak) / theta_k
        B12 = -inv_Ak_u_k / theta_k
        B21 = -v_k_T_inv_Ak / theta_k
        B22 = np.array([[1.0 / theta_k]])

        # Ghép các khối lại
        top_row = np.hstack((B11, B12))
        bottom_row = np.hstack((B21, B22))
        inv_Ak = np.vstack((top_row, bottom_row))

        steps.append({
            "k": k + 1,
            "theta": theta_k,
            "inv_A_k": inv_Ak
        })
        
    check_matrix = A @ inv_Ak

    return {
        "status": "success",
        "inverse": zero_small(inv_Ak, tol),
        "check": zero_small(check_matrix, tol),
        "steps": steps,
        "num_vars": n
    }