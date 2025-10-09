# backend/numerical_methods/linear_algebra/inverse/lu_inverse.py
import numpy as np
import scipy.linalg
from backend.utils.helpers import zero_small

def lu_inverse(A, tol=1e-15):
    """
    Tính ma trận nghịch đảo A⁻¹ bằng cách giải n hệ phương trình Ax = eᵢ
    sử dụng phân rã LU. (Phiên bản đã sửa lỗi thứ tự cột).
    """
    if A.shape[0] != A.shape[1]:
        raise ValueError("Ma trận phải là ma trận vuông.")
    
    n = A.shape[0]
    if abs(np.linalg.det(A)) < tol:
        raise ValueError("Ma trận suy biến (det(A) gần bằng 0), không có nghịch đảo.")

    # Bước 1: Phân rã A = PLU
    P, L, U = scipy.linalg.lu(A)
    
    if np.any(np.abs(np.diag(U)) < tol):
        raise ValueError("Ma trận U có phần tử trên đường chéo bằng 0, không thể tính nghịch đảo.")

    # Bước 2: Ta cần giải AX = I => LUX = P.T @ I
    # Vế phải là P.T (P chuyển vị)
    rhs = P.T 

    # Bước 3: Giải n hệ phương trình để tìm từng cột của A⁻¹
    inv_A_cols = []
    steps_solve = []

    for i in range(n):
        b_col = rhs[:, i] # Lấy từng cột của ma trận P.T
        
        # Giải Ly = b_col (thế xuôi)
        y = scipy.linalg.solve_triangular(L, b_col, lower=True)
        
        # Giải Ux = y (thế ngược)
        x = scipy.linalg.solve_triangular(U, y)
        
        inv_A_cols.append(x)
        steps_solve.append({
            "column_index": i + 1,
            "b_col": zero_small(b_col, tol),
            "y_col": zero_small(y, tol),
            "x_col": zero_small(x, tol)
        })

    # Ghép các cột kết quả lại thành ma trận A⁻¹
    inv_A = np.column_stack(inv_A_cols)
    
    return {
        "status": "success",
        "inverse": zero_small(inv_A, tol),
        "decomposition": {
            "P": zero_small(P, tol),
            "L": zero_small(L, tol),
            "U": zero_small(U, tol)
        },
        "steps_solve": steps_solve,
        "num_vars": n
    }