# backend/numerical_methods/linear_algebra/direct/lu_decomposition.py
import numpy as np
import scipy.linalg
from backend.utils.helpers import zero_small # <<< THÊM DÒNG IMPORT BỊ THIẾU

def _lu_decomposition_steps(A, tol):
    """
    Phân tích LU không pivoting (Doolittle) để lấy các bước trung gian.
    """
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        return [] # Không thực hiện với ma trận không vuông
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    steps = []
    
    for i in range(n):
        for k in range(i, n):
            sum_val = np.dot(L[i, :i], U[:i, k])
            U[i, k] = A[i, k] - sum_val
            
        if abs(U[i, i]) < tol:
            return steps

        L[i, i] = 1
        for k in range(i + 1, n):
            sum_val = np.dot(L[k, :i], U[:i, i])
            L[k, i] = (A[k, i] - sum_val) / U[i, i]
            
        steps.append({'L': L.copy(), 'U': U.copy()})
        
    return steps

def solve_lu(A, b, tol):
    """
    Giải hệ phương trình AX=B bằng phân rã LU.
    """
    if b.ndim == 1:
        b = b.reshape(-1, 1)
    
    m, n = A.shape
    
    lu_steps = _lu_decomposition_steps(A, tol)
    
    P, L, U = None, None, None
    is_square = m == n
    if is_square:
        try:
            P, L, U = scipy.linalg.lu(A)
        except ValueError:
            is_square = False # Coi như không vuông nếu không phân rã được

    rank_A = np.linalg.matrix_rank(A, tol=tol)
    AB = np.hstack((A, b))
    rank_AB = np.linalg.matrix_rank(AB, tol=tol)

    result = { "lu_steps": lu_steps, "num_vars": n, "rank": rank_A }

    if rank_A < rank_AB:
        result.update({"status": "no_solution"})
        
    elif rank_A < n: # Vô số nghiệm
        particular_solution, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        null_space = scipy.linalg.null_space(A)
        result.update({
            "status": "infinite_solutions",
            "particular_solution": zero_small(particular_solution, tol=tol),
            "null_space_vectors": zero_small(null_space, tol=tol)
        })
    else: # Nghiệm duy nhất (hoặc xấp xỉ cho hệ không vuông)
        if is_square:
            Y = scipy.linalg.solve_triangular(L, P @ b, lower=True)
            X = scipy.linalg.solve_triangular(U, Y)
        else: # Dùng least squares cho hệ không vuông có rank = số ẩn
            X, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
            Y = None

        result.update({
            "status": "unique_solution",
            "solution": zero_small(X, tol=tol),
            "intermediate_y": zero_small(Y, tol=tol) if Y is not None else None
        })

    if P is not None:
        result.update({"decomposition": {
            "P": zero_small(P, tol=tol), 
            "L": zero_small(L, tol=tol), 
            "U": zero_small(U, tol=tol)
        }})
        
    return result