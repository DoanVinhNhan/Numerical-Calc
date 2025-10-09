#backend/numerical_methods/linear_algebra/inverse/gauss_jordan_inverse.py
import numpy as np
from backend.numerical_methods.linear_algebra.direct.gauss_jordan import gauss_jordan

def gauss_jordan_inverse(A, tol=1e-15):
    """
    Tính ma trận nghịch đảo của A bằng phương pháp Gauss-Jordan.
    """
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError("Ma trận A phải là ma trận vuông để tính ma trận nghịch đảo.")
    
    I = np.eye(n)
    result = gauss_jordan(A, I, tol)
    
    if result["status"] != "unique_solution":
        raise ValueError("Ma trận A không khả nghịch, không thể tính ma trận nghịch đảo.")
    
    inverse_A = result["solution"]
    
    return {
        "inverse": inverse_A,
        "steps": result["steps"],
        "num_vars": n
    }