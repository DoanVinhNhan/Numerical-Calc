# backend/numerical_methods/linear_algebra/eigen/danilevsky.py
import numpy as np
from backend.utils.helpers import get_char_polynomial

def danilevsky_algorithm(A):
    """
    Thuật toán Danilevsky để tìm trị riêng và vector riêng.
    """
    if A.shape[0] != A.shape[1]:
        raise ValueError('Ma trận đầu vào phải là ma trận vuông.')

    n = A.shape[0]
    similar = A.copy().astype(complex)
    back = np.eye(n, dtype=complex)
    steps_log = [{'desc': 'Ma trận ban đầu', 'matrix': similar.copy()}]

    # Giai đoạn 1: Biến đổi ma trận
    for k in range(n - 1, 0, -1):
        if abs(similar[k, k - 1]) < 1e-9:
            steps_log.append({'desc': f'Hàng {k+1} không cần biến đổi (tạo thành khối riêng).', 'matrix': similar.copy()})
            continue

        M = np.eye(n, dtype=complex)
        M[k - 1, :] = similar[k, :]
        
        if np.linalg.cond(M) > 1/np.finfo(M.dtype).eps:
            raise ValueError(f'Ma trận biến đổi M ở bước k={k} bị suy biến, không thể tiếp tục.')

        M_inv = np.linalg.inv(M)

        similar = M @ similar @ M_inv
        back = back @ M_inv
        steps_log.append({
            'desc': f'Sau khi biến đổi hàng {k+1}.',
            'matrix': similar.copy(),
            'M': M,
            'M_inv': M_inv
        })
        
    steps_log.append({'desc': 'Ma trận cuối (dạng tam giác trên theo khối Frobenius)', 'matrix': similar.copy()})
    
    # Giai đoạn 2: Trích xuất kết quả
    final_eigenvalues = []
    final_eigenvectors = []

    boundaries = [n]
    for k in range(n - 1, 0, -1):
        is_block_boundary = np.all(np.abs(similar[k, :k]) < 1e-9)
        if is_block_boundary:
            boundaries.append(k)

    boundaries.append(0)
    boundaries = sorted(list(set(boundaries)))

    for i in range(len(boundaries) - 1):
        start, end = boundaries[i], boundaries[i+1]
        F_block = similar[start:end, start:end]
        
        poly_coeffs = get_char_polynomial(F_block)
        eigvals = np.roots(poly_coeffs)
        final_eigenvalues.extend(eigvals)
        
        for val in eigvals:
            y_F = np.power(val, np.arange(F_block.shape[0] - 1, -1, -1)).reshape(-1, 1)
            y_similar = np.zeros((n, 1), dtype=complex)
            y_similar[start:end, :] = y_F
            x_A = back @ y_similar
            final_eigenvectors.append(x_A)

    total_char_poly_coeffs = np.poly(final_eigenvalues)

    return {
        'status': 'success',
        'eigenvalues': np.array(final_eigenvalues),
        'eigenvectors': final_eigenvectors,
        'frobenius_matrix': similar,
        'char_poly': total_char_poly_coeffs,
        'steps': steps_log
    }