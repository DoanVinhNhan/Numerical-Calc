import numpy as np
from backend.utils.helpers import zero_small

def solve_cholesky(A, b, tol):
    """
    Giải hệ phương trình AX=B bằng phương pháp Cholesky.
    Tự động xử lý ma trận không đối xứng bằng cách giải AᵀAx = Aᵀb.
    """
    if b.ndim == 1:
        b = b.reshape(-1, 1)

    # --- 1. Kiểm tra đối xứng và chuyển đổi nếu cần ---
    is_symmetric = np.allclose(A, A.T, atol=tol)
    if is_symmetric:
        M = A
        d = b
        transformation_message = "Ma trận A đối xứng, tiến hành phân tách Cholesky trực tiếp."
    else:
        transformation_message = "Ma trận A không đối xứng. Chuyển hệ về dạng AᵀAx = Aᵀb."
        M = A.T @ A
        d = A.T @ b

    # --- 2. Kiểm tra xác định dương ---
    try:
        eigenvalues = np.linalg.eigvalsh(M)
        if np.min(eigenvalues) <= tol:
            raise ValueError("Ma trận (hoặc AᵀA) không xác định dương, không thể phân tích Cholesky.")
    except np.linalg.LinAlgError:
        raise ValueError("Lỗi tính toán giá trị riêng. Ma trận có vấn đề về số học.")

    # --- 3. Phân rã Cholesky (M = UᵀU) ---
    n = M.shape[0]
    U = np.zeros((n, n), dtype=float)
    for i in range(n):
        sum_k = np.dot(U[:i, i], U[:i, i])
        val_inside_sqrt = M[i, i] - sum_k
        if val_inside_sqrt <= tol:
            raise ValueError(f"Phần tử trên đường chéo U[{i},{i}] không dương. Ma trận không xác định dương.")
        
        U[i, i] = np.sqrt(val_inside_sqrt)
        
        for j in range(i + 1, n):
            sum_k = np.dot(U[:i, i], U[:i, j])
            U[i, j] = (M[i, j] - sum_k) / U[i, i]
    
    Ut = U.T

    # --- 4. Giải hệ phương trình ---
    # Giải Uᵀy = d
    y = np.linalg.solve(Ut, d)
    # Giải Ux = y
    x = np.linalg.solve(U, y)

    return {
        "status": "unique_solution",
        "transformation_message": transformation_message,
        "solution": zero_small(x, tol=tol),
        "decomposition": {
            "M": zero_small(M, tol=tol) if not is_symmetric else None,
            "d": zero_small(d, tol=tol) if not is_symmetric else None,
            "U": zero_small(U, tol=tol),
            "Ut": zero_small(Ut, tol=tol)
        },
        "intermediate_y": zero_small(y, tol=tol),
    }