# backend/numerical_methods/linear_algebra/inverse/cholesky_inverse.py
import numpy as np
import scipy.linalg
from backend.utils.helpers import zero_small

def cholesky_inverse(A, tol=1e-15):
    """
    Tính ma trận nghịch đảo A⁻¹ bằng phương pháp Cholesky, tái sử dụng
    logic phân rã đã có.
    - Nếu A không đối xứng, tính (AᵀA)⁻¹Aᵀ.
    """
    if A.shape[0] != A.shape[1]:
        raise ValueError("Ma trận phải là ma trận vuông.")

    is_symmetric = np.allclose(A, A.T, atol=tol)
    
    M = A
    transformation_message = "Ma trận A đối xứng, tiến hành phân tích Cholesky trực tiếp."
    if not is_symmetric:
        M = A.T @ A
        transformation_message = "Ma trận A không đối xứng. Chuyển sang tính M = AᵀA."

    # Bước 1: Phân rã Cholesky: M = UᵀU (Tái sử dụng logic từ file cholesky.py)
    try:
        eigenvalues = np.linalg.eigvalsh(M)
        if np.min(eigenvalues) <= tol:
            raise ValueError("Ma trận (hoặc AᵀA) không xác định dương, không thể phân tích Cholesky.")
    except np.linalg.LinAlgError:
        raise ValueError("Lỗi tính toán giá trị riêng. Ma trận có vấn đề về số học.")

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

    # Bước 2: Tìm nghịch đảo của U (ma trận tam giác trên) bằng cách giải UX = I
    I = np.eye(n)
    inv_U = scipy.linalg.solve_triangular(U, I)

    # Bước 3: Tính nghịch đảo của M: M⁻¹ = U⁻¹(U⁻¹)ᵀ
    inv_M = inv_U @ inv_U.T
    
    # Bước 4: Tính A⁻¹
    if is_symmetric:
        inv_A = inv_M
        final_message = "Tính ma trận nghịch đảo A⁻¹ thành công."
    else:
        inv_A = inv_M @ A.T
        final_message = "Tính ma trận nghịch đảo A⁻¹ = (AᵀA)⁻¹Aᵀ thành công."
        
    return {
        "status": "success",
        "inverse": zero_small(inv_A, tol),
        "is_symmetric": is_symmetric,
        "transformation_message": transformation_message,
        "final_message": final_message,
        "intermediates": {
            "M": zero_small(M, tol) if not is_symmetric else None,
            "U": zero_small(U, tol),
            "Ut": zero_small(U.T, tol),
            "U_inv": zero_small(inv_U, tol),
            "M_inv": zero_small(inv_M, tol)
        },
        "num_vars": n
    }