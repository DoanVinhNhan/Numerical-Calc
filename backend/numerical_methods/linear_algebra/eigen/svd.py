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

def calculate_svd_approximation(A, method='rank-k', **kwargs):
    """
    Tính toán xấp xỉ ma trận A bằng SVD dựa trên các phương pháp khác nhau.
    """
    try:
        A = np.array(A, dtype=float)
        if A.ndim != 2:
            return {"success": False, "error": "Đầu vào phải là một ma trận 2D."}

        U, s, Vt = np.linalg.svd(A, full_matrices=False)
        original_rank = np.sum(s > 1e-10)
        
        A_norm = np.linalg.norm(A)

        k = 0
        method_used = ""
        info = {}

        if method == 'rank-k':
            k = int(kwargs.get('k', 1))
            if k > len(s) or k < 1:
                return {"success": False, "error": f"Hạng k phải nằm trong khoảng [1, {len(s)}]."}
            method_used = f"Xấp xỉ hạng k={k}"
            info['k_requested'] = k

        elif method == 'threshold':
            threshold = float(kwargs.get('threshold', 0.1))
            k = np.sum(s >= threshold)
            if k == 0:
                k = 1 
            method_used = f"Giữ giá trị kỳ dị >= {threshold}"
            info['threshold'] = threshold

        elif method == 'error-bound':
            relative_error_bound = float(kwargs.get('error_bound', 0.01))
            method_used = f"Sai số tương đối <= {relative_error_bound*100:.2f}%"
            info['target_relative_error_bound'] = relative_error_bound

            if A_norm == 0:
                k = 0
            else:
                target_absolute_error_norm_sq = (relative_error_bound * A_norm) ** 2
                
                k = len(s)
                cumulative_error_norm_sq = 0
                
                for i in range(len(s) - 1, -1, -1):
                    if cumulative_error_norm_sq + s[i]**2 < target_absolute_error_norm_sq:
                        cumulative_error_norm_sq += s[i]**2
                        k -= 1
                    else:
                        break 
                
                if k == 0: k = 1

        A_approx = np.dot(U[:, :k], np.dot(np.diag(s[:k]), Vt[:k, :]))

        error_matrix = A - A_approx
        absolute_error = np.linalg.norm(error_matrix)
        relative_error = (absolute_error / A_norm) * 100 if A_norm > 0 else 0

        total_energy = np.sum(s**2)
        retained_energy = np.sum(s[:k]**2)
        info['energy_ratio'] = (retained_energy / total_energy) * 100 if total_energy > 0 else 100
        
        retained_components = [{"index": int(i + 1), "singular_value": float(val), "contribution": float((val**2/total_energy)*100) if total_energy > 0 else 0.0} for i, val in enumerate(s[:k])]
        discarded_components = [{"index": int(i + 1), "singular_value": float(val), "contribution": float((val**2/total_energy)*100) if total_energy > 0 else 0.0} for i, val in enumerate(s[k:], start=k)]

        return {
            "success": True,
            "method_used": method_used,
            "original_matrix": A.tolist(),
            "approximated_matrix": A_approx.tolist(),
            "error_matrix": error_matrix.tolist(),
            "original_rank": int(original_rank),
            "effective_rank": int(k),
            "absolute_error": float(absolute_error),
            "relative_error": float(relative_error),
            "retained_components": retained_components,
            "discarded_components": discarded_components,
            "detailed_info": info
        }

    except Exception as e:
        return {"success": False, "error": f"Lỗi tính toán: {str(e)}"}
