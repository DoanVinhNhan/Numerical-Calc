import numpy as np
from backend.utils.helpers import zero_small

def gauss_jordan(A, b, tol):
    """
    Giải hệ phương trình AX = B bằng phương pháp khử Gauss-Jordan,
    tuân thủ quy tắc chọn pivot đặc biệt và xử lý đầy đủ các trường hợp nghiệm.
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
    pivoted_rows = []
    pivoted_cols = []
    
    max_pivots = min(num_rows, num_vars)
    for step in range(max_pivots):
        pivot_r, pivot_c = -1, -1
        
        # --- 2. Chọn Pivot theo quy tắc đặc biệt ---
        # Ưu tiên tìm pivot là +-1.0
        found_one = False
        for r in range(num_rows):
            if r in pivoted_rows: continue
            for c in range(num_vars):
                if c in pivoted_cols: continue
                if (float(augmented_matrix[r, c]) == 1.0) or (float(augmented_matrix[r, c]) == -1.0):
                    pivot_r, pivot_c = r, c
                    found_one = True
                    break
            if found_one: break
            
        # Nếu không có +-1.0, tìm pivot có giá trị tuyệt đối lớn nhất
        if not found_one:
            max_val = tol
            for r in range(num_rows):
                if r in pivoted_rows: continue
                for c in range(num_vars):
                    if c in pivoted_cols: continue
                    if abs(augmented_matrix[r, c]) > max_val:
                        max_val = abs(augmented_matrix[r, c])
                        pivot_r, pivot_c = r, c
                        
        # Nếu không tìm thấy pivot nào nữa, dừng lại
        if pivot_r == -1:
            break
            
        pivot_element = augmented_matrix[pivot_r, pivot_c]
        pivoted_rows.append(pivot_r)
        pivoted_cols.append(pivot_c)
        steps.append({"type": "pivot_selection", "pivot_row": pivot_r, "pivot_col": pivot_c, "pivot_value": pivot_element, "matrix": augmented_matrix.copy()})
        
        # --- 3. Quá trình khử ---
        # Chuẩn hóa hàng pivot
        augmented_matrix[pivot_r, :] /= pivot_element
        
        # Khử các phần tử khác trong cột pivot (cả trên và dưới)
        for i in range(num_rows):
            if i != pivot_r:
                factor = augmented_matrix[i, pivot_c]
                if abs(factor) > tol:
                    augmented_matrix[i, :] -= factor * augmented_matrix[pivot_r, :]
        
        augmented_matrix = zero_small(augmented_matrix, tol=tol)
        steps.append({"type": "elimination", "pivot_row": pivot_r, "pivot_col": pivot_c, "matrix": augmented_matrix.copy()})

    # --- 4. Kết luận nghiệm ---
    rank = len(pivoted_rows)
    # Kiểm tra vô nghiệm
    for r in range(num_rows):
        is_A_part_zero = np.all(np.abs(augmented_matrix[r, :num_vars]) < tol)
        is_b_part_nonzero = np.any(np.abs(augmented_matrix[r, num_vars:]) > tol)
        if is_A_part_zero and is_b_part_nonzero:
            return {"status": "no_solution", "steps": steps}

    # Sắp xếp lại các pivot để dễ dàng truy xuất
    pivots_map = sorted(zip(pivoted_cols, pivoted_rows))
    pivoted_cols_sorted = [p[0] for p in pivots_map]
    pivoted_rows_sorted = [p[1] for p in pivots_map]

    # Vô số nghiệm
    if rank < num_vars:
        free_vars_indices = [i for i in range(num_vars) if i not in pivoted_cols_sorted]
        
        particular_solution = np.zeros((num_vars, b_float.shape[1]))
        for i, r_idx in enumerate(pivoted_rows_sorted):
            pivot_col = pivoted_cols_sorted[i]
            particular_solution[pivot_col, :] = augmented_matrix[r_idx, num_vars:]
            
        null_space_vectors = np.zeros((num_vars, len(free_vars_indices)))
        for k, free_idx in enumerate(free_vars_indices):
            null_space_vectors[free_idx, k] = 1.0
            for i, r_idx in enumerate(pivoted_rows_sorted):
                pivot_col = pivoted_cols_sorted[i]
                null_space_vectors[pivot_col, k] = -augmented_matrix[r_idx, free_idx]
        
        return {
            "status": "infinite_solutions", "rank": rank, "num_vars": num_vars,
            "particular_solution": zero_small(particular_solution, tol=tol),
            "null_space_vectors": zero_small(null_space_vectors, tol=tol),
            "steps": steps
        }
    
    # Nghiệm duy nhất
    else:
        solution = np.zeros((num_vars, b_float.shape[1]))
        for i, r_idx in enumerate(pivoted_rows_sorted):
            pivot_col = pivoted_cols_sorted[i]
            solution[pivot_col, :] = augmented_matrix[r_idx, num_vars:]
        
        return {
            "status": "unique_solution",
            "solution": zero_small(solution, tol=tol),
            "steps": steps
        }