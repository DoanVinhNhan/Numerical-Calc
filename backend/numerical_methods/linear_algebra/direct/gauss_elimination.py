# backend/numerical_methods/linear_algebra/direct/gauss_elimination.py
import numpy as np
from backend.utils.helpers import zero_small

def gauss_elimination(A, b, tol):
    """
    Giải hệ phương trình tuyến tính Ax = b bằng phương pháp khử Gauss,
    sử dụng chiến lược hoán vị-nếu-trụ-bằng-0.
    Hàm này xử lý các trường hợp vô nghiệm và vô số nghiệm.

    Args:
        A (np.ndarray): Ma trận hệ số.
        b (np.ndarray): Vector/Ma trận hằng số.
        tol (float): Ngưỡng để coi một số là zero. Giá trị này được
                     truyền từ API route dựa trên cài đặt của người dùng.

    Returns:
        dict: Một từ điển chứa kết quả tính toán có cấu trúc.
    """
    # --- 1. Chuẩn bị ---
    A_float = A.copy().astype(float)
    b_float = b.copy().astype(float)
    if b_float.ndim == 1:
        b_float = b_float.reshape(-1, 1)

    augmented_matrix = np.hstack([A_float, b_float])
    num_rows, num_cols_aug = augmented_matrix.shape
    num_vars = A.shape[1]
    
    steps = []
    pivot_columns = []
    pivot_row = 0
    col_index = 0

    # --- 2. Quá trình khử xuôi (Forward Elimination) ---
    while pivot_row < num_rows and col_index < num_vars:
        # Nếu phần tử trụ bằng 0, tìm một hàng khác để hoán vị
        if abs(augmented_matrix[pivot_row, col_index]) < tol:
            swap_with_row = -1
            for k in range(pivot_row + 1, num_rows):
                if abs(augmented_matrix[k, col_index]) > tol:
                    swap_with_row = k
                    break
            
            if swap_with_row != -1:
                augmented_matrix[[pivot_row, swap_with_row]] = augmented_matrix[[swap_with_row, pivot_row]]
                steps.append({
                    "type": "pivot", "from_row": swap_with_row, "to_row": pivot_row,
                    "matrix": augmented_matrix.copy()
                })

        pivot_element = augmented_matrix[pivot_row, col_index]

        # Nếu phần tử trụ vẫn bằng 0 (cả cột dưới nó đều là 0), bỏ qua cột này
        if abs(pivot_element) < tol:
            col_index += 1
            continue

        pivot_columns.append(col_index)
        
        # Khử các phần tử bên dưới trụ
        for i in range(pivot_row + 1, num_rows):
            factor = augmented_matrix[i, col_index] / pivot_element
            if abs(factor) > tol:
                augmented_matrix[i, :] -= factor * augmented_matrix[pivot_row, :]
        
        # Sử dụng hàm tiện ích để làm tròn các giá trị nhỏ về 0
        augmented_matrix = zero_small(augmented_matrix, tol=tol)
        steps.append({
            "type": "elimination", "pivot_row": pivot_row, "pivot_col": col_index,
            "matrix": augmented_matrix.copy()
        })
        
        pivot_row += 1
        col_index += 1

    rank = len(pivot_columns)

    # --- 3. Kiểm tra nghiệm ---
    for r in range(rank, num_rows):
        if np.any(np.abs(augmented_matrix[r, num_vars:]) > tol):
            return {"status": "no_solution", "steps": steps}

    # --- 4. Quá trình thế ngược (Back Substitution) ---
    # Vô số nghiệm
    if rank < num_vars:
        free_vars_indices = [i for i in range(num_vars) if i not in pivot_columns]
        
        particular_solution = np.zeros((num_vars, b_float.shape[1]))
        y = augmented_matrix[:, num_vars:]
        for i in range(rank - 1, -1, -1):
            pivot_col = pivot_columns[i]
            sum_val = augmented_matrix[i, pivot_col+1:num_vars] @ particular_solution[pivot_col+1:, :]
            particular_solution[pivot_col, :] = (y[i, :] - sum_val) / augmented_matrix[i, pivot_col]

        null_space_vectors = []
        for free_idx in free_vars_indices:
            v = np.zeros(num_vars)
            v[free_idx] = 1
            for i in range(rank - 1, -1, -1):
                pivot_col = pivot_columns[i]
                sum_val = np.dot(augmented_matrix[i, pivot_col+1:num_vars], v[pivot_col+1:])
                v[pivot_col] = -sum_val / augmented_matrix[i, pivot_col]
            null_space_vectors.append(v)
        
        return {
            "status": "infinite_solutions", "rank": rank, "num_vars": num_vars,
            "particular_solution": zero_small(particular_solution, tol=tol),
            "null_space_vectors": zero_small(np.array(null_space_vectors).T, tol=tol),
            "steps": steps
        }

    # Nghiệm duy nhất
    else:
        solution = np.zeros_like(b_float)
        backward_steps = []
        for i in range(rank - 1, -1, -1):
            sum_ax = augmented_matrix[i, i+1:num_vars] @ solution[i+1:, :]
            x_i_row = (augmented_matrix[i, num_vars:] - sum_ax) / augmented_matrix[i, i]
            solution[i, :] = x_i_row
            backward_steps.append({"row": i, "solution_so_far": solution.copy()})
            
        return {
            "status": "unique_solution",
            "solution": zero_small(solution, tol=tol),
            "steps": steps, 
            "backward_steps": backward_steps
        }