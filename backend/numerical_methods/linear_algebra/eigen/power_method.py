# backend/numerical_methods/linear_algebra/eigen/power_method.py
import numpy as np

def power_method_single(A, x0=None, tol=1e-9, max_iter=100):
    """
    Tìm giá trị riêng trội và vector riêng tương ứng của ma trận A.
    """
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError("Ma trận phải là ma trận vuông.")

    if x0 is not None:
        x = np.array(x0, dtype=float).reshape((n, 1))
        if np.linalg.norm(x) == 0: # Tránh vector không
            x = np.ones((n, 1), dtype=float)
    else:
        x = np.ones((n, 1), dtype=float)
    x = x / np.linalg.norm(x)

    steps = []
    lambda_old = 0.0

    for i in range(max_iter):
        Ax = A @ x
        norm_Ax = np.linalg.norm(Ax)
        
        if norm_Ax < 1e-12: # Vector lặp tiến về không
            return {
                "status": "success_zero",
                "eigenvalue": 0.0,
                "eigenvector": x,
                "steps": steps
            }
            
        x_new = Ax / norm_Ax
        lambda_new = float(x_new.T @ A @ x_new)

        steps.append({
            'k': i + 1,
            'x_k': x,
            'Ax_k': Ax,
            'lambda_k': lambda_new
        })

        if np.abs(lambda_new - lambda_old) < tol:
            return {
                "status": "success",
                "eigenvalue": lambda_new,
                "eigenvector": x_new,
                "steps": steps,
                "iterations": i + 1
            }
            
        lambda_old = lambda_new
        x = x_new

    raise ValueError(f"Phương pháp không hội tụ sau {max_iter} lần lặp.")


def power_method_deflation(A, num_values=None, x0=None, tol=1e-6, max_iter=100):
    """
    Tìm nhiều giá trị riêng bằng phương pháp Lũy thừa kết hợp Xuống thang (Hotelling's deflation).
    """
    if A.shape[0] != A.shape[1]:
        raise ValueError("Ma trận phải là ma trận vuông.")
    
    n = A.shape[0]
    num_values = num_values if num_values is not None and 0 < num_values <= n else n
    
    A_current = A.copy().astype(float)
    eigen_pairs = []
    all_steps = []

    for s in range(num_values):
        # Sử dụng vector x0 cho lần lặp đầu tiên, sau đó dùng vector ngẫu nhiên
        initial_vector = x0 if s == 0 else None
        
        try:
            result = power_method_single(A_current, x0=initial_vector, tol=tol, max_iter=max_iter)
        except ValueError as e:
            # Dừng nếu ma trận con không hội tụ
            break 

        lambda_val = result['eigenvalue']
        eigenvector = result['eigenvector']
        
        # Vector riêng tìm được là của ma trận A_current, cần tìm lại vector riêng cho ma trận A gốc
        # bằng phương pháp lặp nghịch đảo (inverse iteration)
        try:
            shifted_A = A - lambda_val * np.eye(n)
            v = eigenvector.copy() # Bắt đầu với vector tìm được
            for _ in range(5): # Vài lần lặp là đủ
                v_new = np.linalg.solve(shifted_A, v)
                v = v_new / np.linalg.norm(v_new)
        except np.linalg.LinAlgError:
            v = eigenvector # Nếu lỗi, tạm dùng vector cũ

        eigen_pairs.append({'eigenvalue': lambda_val, 'eigenvector': v})
        
        all_steps.append({
            "eigenvalue_index": s + 1,
            "matrix_before_deflation": A_current.copy(),
            "iteration_details": result['steps']
        })
        
        # Thực hiện xuống thang Hotelling
        A_current = A_current - lambda_val * (v @ v.T)

    if not eigen_pairs:
        raise ValueError("Không tìm thấy giá trị riêng nào.")

    return {
        "status": "success",
        "eigen_pairs": eigen_pairs,
        "steps": all_steps
    }