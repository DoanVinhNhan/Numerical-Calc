# backend/numerical_methods/linear_algebra/direct/gauss_elimination.py
import numpy as np
from backend.utils.helpers import zero_small

def gauss_elimination(A, b, tol):
    """
    Giải hệ phương trình tuyến tính Ax = b bằng phương pháp khử Gauss.
    Hàm này đã được sửa để xử lý đúng các ma trận không vuông.
    """
    # --- 1. Chuẩn bị (Không đổi) ---
    A_float = A.copy().astype(float)
    b_float = b.copy().astype(float)
    if b_float.ndim == 1:
        b_float = b_float.reshape(-1, 1)

    augmented_matrix = np.hstack([A_float, b_float])
    num_rows, num_cols_aug = augmented_matrix.shape
    num_vars = A.shape[1]
    
    steps, pivot_columns, pivot_row, col_index = [], [], 0, 0

    # --- 2. Quá trình khử xuôi (Không đổi) ---
    while pivot_row < num_rows and col_index < num_vars:
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

        if abs(pivot_element) < tol:
            col_index += 1
            continue

        pivot_columns.append(col_index)
        
        for i in range(pivot_row + 1, num_rows):
            factor = augmented_matrix[i, col_index] / pivot_element
            if abs(factor) > tol:
                augmented_matrix[i, :] -= factor * augmented_matrix[pivot_row, :]
        
        augmented_matrix = zero_small(augmented_matrix, tol=tol)
        steps.append({
            "type": "elimination", "pivot_row": pivot_row, "pivot_col": col_index,
            "matrix": augmented_matrix.copy()
        })
        
        pivot_row += 1
        col_index += 1

    rank = len(pivot_columns)

    # --- 3. Kiểm tra nghiệm (Không đổi) ---
    # Logic này sẽ được bổ sung ở bước 4 cho trường hợp rank == num_vars
    
    # --- 4. Quá trình thế ngược (ĐÃ SỬA ĐỔI) ---
    # Vô số nghiệm
    if rank < num_vars:
        # Kiểm tra tính nhất quán cho trường hợp vô số nghiệm
        for r in range(rank, num_rows):
            if np.any(np.abs(augmented_matrix[r, num_vars:]) > tol):
                return {"status": "no_solution", "steps": steps}
        
        # Logic tính nghiệm vô số nghiệm (vẫn đúng)
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

    # Nghiệm duy nhất hoặc Vô nghiệm (trường hợp rank == num_vars)
    else:
        # SỬA LỖI 1: Thêm kiểm tra tính nhất quán cho hệ thừa phương trình
        # Ví dụ: sau khi khử, có hàng [0, 0, 0 | 5], nghĩa là 0 = 5 -> Vô nghiệm
        for r in range(rank, num_rows):
            if np.any(np.abs(augmented_matrix[r, num_vars:]) > tol):
                return {"status": "no_solution", "steps": steps}
        
        # SỬA LỖI 2: Khởi tạo ma trận nghiệm với kích thước đúng
        # Kích thước phải là (số ẩn x số cột của B), không phải shape của B
        solution = np.zeros((num_vars, b_float.shape[1]))
        backward_steps = []
        
        for i in range(rank - 1, -1, -1):
            pivot_col = pivot_columns[i]
            # Tính tổng các thành phần đã biết (A_ij * x_j)
            sum_ax = augmented_matrix[i, pivot_col + 1:num_vars] @ solution[pivot_col + 1:, :]
            
            # Tính nghiệm cho biến hiện tại
            x_i_row = (augmented_matrix[i, num_vars:] - sum_ax) / augmented_matrix[i, pivot_col]
            
            # Gán vào đúng vị trí trong ma trận nghiệm
            solution[pivot_col, :] = x_i_row
            
            backward_steps.append({"row": pivot_col, "solution_so_far": solution.copy()})
            
        return {
            "status": "unique_solution",
            "solution": zero_small(solution, tol=tol),
            "steps": steps, 
            "backward_steps": backward_steps
        }