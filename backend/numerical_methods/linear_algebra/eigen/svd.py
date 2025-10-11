# backend/numerical_methods/linear_algebra/eigen/svd.py
import numpy as np
from backend.utils.helpers import zero_small

def svd_power_deflation(A, num_singular=None, max_iter=20, tol=1e-15, y_init=None):
    """
    Tính SVD của ma trận A bằng phương pháp power method + deflation.
    """
    A = np.array(A, dtype=float)
    m, n = A.shape
    
    # Quyết định làm việc với A^T*A hay A*A^T để tối ưu
    if m >= n:
        Matrix_work = A.T @ A
        vector_size = n
        use_ATA = True
    else:
        Matrix_work = A @ A.T
        vector_size = m
        use_ATA = False
        
    Matrix_work_original = Matrix_work.copy()
    singular_values = []
    vectors = []
    steps = []
    
    max_singular = min(m, n)
    k = num_singular if num_singular is not None and num_singular > 0 else max_singular
    k = min(k, max_singular)
    
    for s in range(k):
        if s == 0 and y_init is not None:
            y = np.array(y_init).reshape(-1, 1)
            if y.shape[0] != vector_size:
                raise ValueError(f"Vector khởi đầu phải có kích thước ({vector_size}, 1) hoặc ({vector_size},)")
            y = y / np.linalg.norm(y)
        else:
            y = np.random.rand(vector_size, 1)
            y = y / np.linalg.norm(y)
            
        y_steps = [y.copy()]
        lambda_steps = []
        matrix_before_deflation = Matrix_work.copy()
        
        lambda_val = 0.0
        for i in range(max_iter):
            y_new = Matrix_work @ y
            norm_y_new = np.linalg.norm(y_new)
            
            if norm_y_new < tol:
                break
                
            y_new = y_new / norm_y_new
            lambda_new = float(y_new.T @ Matrix_work @ y_new)
            
            y = y_new
            y_steps.append(y.copy())
            lambda_steps.append(lambda_new)
            
            if i > 0 and abs(lambda_steps[-1] - lambda_steps[-2]) < tol:
                break
        
        if not lambda_steps or lambda_steps[-1] < tol:
            break
            
        lambda_val = lambda_steps[-1]
        singular = np.sqrt(abs(lambda_val))
        singular_values.append(singular)
        
        vectors.append(y.copy())
        
        # Deflation
        Matrix_work = Matrix_work - lambda_val * (y @ y.T)
        
        steps.append({
            'singular_index': s + 1,
            'matrix_before_deflation': matrix_before_deflation,
            'matrix_after_deflation': Matrix_work.copy(),
            'lambda_steps': lambda_steps,
            'y_steps': y_steps,
            'eigenvalue': lambda_val,
            'singular_value': singular,
            'eigenvector': y,
        })

    if not singular_values:
        raise ValueError('Không thể tìm được giá trị kỳ dị nào với các tham số đã cho.')
        
    if use_ATA:
        V = np.hstack(vectors)
        U_list = [A @ v / s for s, v in zip(singular_values, vectors)]
        U = np.hstack(U_list)
    else:
        U = np.hstack(vectors)
        V_list = [A.T @ u / s for s, u in zip(singular_values, vectors)]
        V = np.hstack(V_list)

    Sigma_diag = np.array(singular_values)
    
    return {
        "status": "success",
        "U": U, "Sigma_diag": Sigma_diag, "Vt": V.T,
        "method": "Power Method & Deflation",
        "intermediate_steps": {
            'matrix_used_info': f"{'AᵀA' if use_ATA else 'AAᵀ'} (kích thước {Matrix_work_original.shape})",
            'original_matrix': Matrix_work_original,
            'steps': steps
        }
    }

def svd_numpy(A):
    """
    Tính SVD bằng numpy (chuẩn).
    """
    if A.size == 0:
        raise ValueError("Ma trận đầu vào không được rỗng.")
    
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    
    return {
        "status": "success",
        "U": U, "Sigma_diag": s, "Vt": Vt,
        "method": "NumPy Standard",
        "intermediate_steps": None
    }