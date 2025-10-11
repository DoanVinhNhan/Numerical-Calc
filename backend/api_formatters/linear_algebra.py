# backend/api_formatters/linear_algebra.py
import numpy as np

def format_gauss_elimination_result(result):
    num_vars = result.get('num_vars', -1)
    steps_formatted = []
    step_counter = 1
    for step_data in result['steps']:
        message = ""
        if step_data['type'] == 'pivot':
            message = f"<b>Bước {step_counter}:</b> Hoán vị hàng {step_data['to_row'] + 1} và {step_data['from_row'] + 1}."
        elif step_data['type'] == 'elimination':
            message = f"<b>Bước {step_counter}:</b> Dùng hàng {step_data['pivot_row']+1} để khử các phần tử trong cột {step_data['pivot_col']+1}."
        steps_formatted.append({"message": message, "matrix": step_data['matrix'].tolist(), "num_vars": num_vars})
        step_counter += 1

    if result['status'] == 'no_solution':
        return {"method": "Khử Gauss", "status": "no_solution", "message": "Hệ phương trình vô nghiệm.", "steps": steps_formatted}
    elif result['status'] == 'infinite_solutions':
        return {"method": "Khử Gauss", "status": "infinite_solutions", "message": f"Hệ có vô số nghiệm (Hạng = {result['rank']} < Số ẩn = {result['num_vars']}).", "steps": steps_formatted, "general_solution": {"particular_solution": result['particular_solution'].tolist(), "null_space_vectors": result['null_space_vectors'].tolist()}}
    elif result['status'] == 'unique_solution':
        backward_steps_formatted = [{"message": f"Tính toán cho biến x<sub>{bs_step['row']+1}</sub>.", "solution_so_far": bs_step['solution_so_far'].tolist()} for bs_step in result.get('backward_steps', [])]
        return {"method": "Khử Gauss", "status": "unique_solution", "message": "Hệ phương trình có nghiệm duy nhất.", "solution": result['solution'].tolist(), "steps": steps_formatted, "backward_steps": backward_steps_formatted}
    return {"error": "Lỗi không xác định."}

def format_gauss_jordan_result(result):
    num_vars = result.get('num_vars', -1)
    steps_formatted = []
    step_counter = 1
    for step_data in result['steps']:
        message = ""
        if step_data['type'] == 'pivot_selection':
            pv, pr, pc = step_data['pivot_value'], step_data['pivot_row'] + 1, step_data['pivot_col'] + 1
            message = f"<b>Bước {step_counter}:</b> Chọn pivot là {pv:.4f} tại ({pr}, {pc})."
        elif step_data['type'] == 'elimination':
            pc = step_data['pivot_col'] + 1
            message = f"<b>Bước {step_counter}:</b> Chuẩn hóa hàng pivot và khử các phần tử trong cột {pc}."
        steps_formatted.append({"message": message, "matrix": step_data['matrix'].tolist(), "num_vars": num_vars})
        step_counter += 1

    if result['status'] == 'no_solution':
        return {"method": "Gauss-Jordan", "status": "no_solution", "message": "Hệ phương trình vô nghiệm.", "steps": steps_formatted}
    elif result['status'] == 'infinite_solutions':
        return {"method": "Gauss-Jordan", "status": "infinite_solutions", "message": f"Hệ có vô số nghiệm (Hạng = {result['rank']} < Số ẩn = {result['num_vars']}).", "steps": steps_formatted, "general_solution": {"particular_solution": result['particular_solution'].tolist(), "null_space_vectors": result['null_space_vectors'].tolist()}}
    elif result['status'] == 'unique_solution':
        return {"method": "Gauss-Jordan", "status": "unique_solution", "message": "Hệ phương trình có nghiệm duy nhất.", "solution": result['solution'].tolist(), "steps": steps_formatted}
    return {"error": "Lỗi không xác định."}


def format_lu_result(result):
    formatted = {"method": "Phân rã LU"}
    
    # Định dạng các bước trung gian
    steps_formatted = []
    for i, step in enumerate(result.get('lu_steps', [])):
        steps_formatted.append({
            "message": f"<b>Bước {i+1}:</b> Tính hàng {i+1} của U và cột {i+1} của L.",
            "L": step['L'].tolist(), # Dữ liệu đã được làm sạch
            "U": step['U'].tolist()  # Dữ liệu đã được làm sạch
        })
    formatted['steps'] = steps_formatted

    # Xử lý các trạng thái
    status = result['status']
    formatted['status'] = status
    
    if status == "no_solution":
        formatted['message'] = f"Hệ vô nghiệm (hạng(A)={result['rank']} < hạng([A|B]))."
    elif status == "infinite_solutions":
        formatted['message'] = f"Hệ có vô số nghiệm (hạng(A)={result['rank']} < số ẩn={result['num_vars']})."
        formatted['general_solution'] = {
            "particular_solution": result['particular_solution'].tolist(),
            "null_space_vectors": result['null_space_vectors'].tolist()
        }
    elif status == "unique_solution":
        formatted['message'] = f"Hệ có nghiệm duy nhất (hoặc nghiệm xấp xỉ tốt nhất)."
        formatted['solution'] = result['solution'].tolist()
        if 'intermediate_y' in result and result['intermediate_y'] is not None:
            formatted['intermediate_y'] = result['intermediate_y'].tolist()

    # Thêm ma trận P, L, U nếu có
    if 'decomposition' in result:
        decomp = result['decomposition']
        formatted['decomposition'] = {
            "P": decomp['P'].tolist(),
            "L": decomp['L'].tolist(),
            "U": decomp['U'].tolist()
        }
    return formatted

def format_cholesky_result(result):
    formatted = {
        "method": "Cholesky",
        "status": result['status'],
        "message": "Hệ có nghiệm duy nhất tìm bằng phân tách Cholesky.",
        "transformation_message": result['transformation_message'],
        "solution": result['solution'].tolist(),
        "intermediate_y": result['intermediate_y'].tolist()
    }

    decomp = result['decomposition']
    formatted_decomp = {
        "U": decomp['U'].tolist(),
        "Ut": decomp['Ut'].tolist()
    }
    if decomp.get('M') is not None:
        formatted_decomp['M'] = decomp['M'].tolist()
    if decomp.get('d') is not None:
        formatted_decomp['d'] = decomp['d'].tolist()
    
    formatted['decomposition'] = formatted_decomp
    return formatted

def format_inverse_gauss_jordan_result(result):
    """
    Định dạng kết quả tính ma trận nghịch đảo bằng phương pháp Gauss-Jordan.
    """
    formatted = {
        "method": "Ma trận nghịch đảo (Gauss-Jordan)",
        "status": "success",
        "message": f"Tính ma trận nghịch đảo thành công cho ma trận {result['num_vars']}x{result['num_vars']}.",
        "inverse": result['inverse'].tolist()
    }

    # Định dạng các bước tính toán
    num_vars = result.get('num_vars', -1)
    steps_formatted = []
    step_counter = 1
    for step_data in result['steps']:
        message = ""
        if step_data['type'] == 'pivot_selection':
            pv, pr, pc = step_data['pivot_value'], step_data['pivot_row'] + 1, step_data['pivot_col'] + 1
            message = f"<b>Bước {step_counter}:</b> Chọn pivot là {pv:.4f} tại ({pr}, {pc})."
        elif step_data['type'] == 'elimination':
            pc = step_data['pivot_col'] + 1
            message = f"<b>Bước {step_counter}:</b> Chuẩn hóa hàng pivot và khử các phần tử trong cột {pc}."
        steps_formatted.append({"message": message, "matrix": step_data['matrix'].tolist(), "num_vars": num_vars})
        step_counter += 1

    formatted['steps'] = steps_formatted
    return formatted

def format_lu_inverse_result(result):
    """
    Định dạng kết quả tính ma trận nghịch đảo bằng phân rã LU (phiên bản đã sửa lỗi).
    """
    if result.get('status') != 'success':
        return {"error": result.get('error', 'Lỗi không xác định')}

    decomp = result['decomposition']
    
    # Bước 1: Phân rã
    steps = [{
        "message": "<b>Bước 1:</b> Phân rã A = PLU",
        "P": decomp['P'].tolist(),
        "L": decomp['L'].tolist(),
        "U": decomp['U'].tolist(),
    }]
    
    # Các bước giải hệ phương trình
    steps.append({
        "message": "<b>Bước 2:</b> Với mỗi cột eᵢ của ma trận đơn vị, giải hệ LUX = Pᵀeᵢ để tìm cột xᵢ của A⁻¹."
    })

    for step_solve in result['steps_solve']:
        i = step_solve['column_index']
        steps.append({
            "message": f"<b>Bước 2.{i}:</b> Tìm cột {i} của A⁻¹",
            "solve_process": f"Giải LY=Pᵀeᵢ, sau đó UX=Y",
            "Y_col": np.array(step_solve['y_col']).reshape(-1, 1).tolist(),
            "X_col": np.array(step_solve['x_col']).reshape(-1, 1).tolist(),
        })

    # Bước cuối: Ma trận nghịch đảo hoàn chỉnh
    steps.append({
        "message": "<b>Bước 3:</b> Ghép các vector cột X đã tìm được để tạo thành ma trận A⁻¹."
    })

    return {
        "method": "Ma trận nghịch đảo (Phân rã LU)",
        "status": "success",
        "message": f"Tính ma trận nghịch đảo bằng phân rã LU thành công.",
        "inverse": result['inverse'].tolist(),
        "steps": steps
    }

def format_cholesky_inverse_result(result):
    """
    Định dạng kết quả tính ma trận nghịch đảo bằng Cholesky.
    """
    inter = result['intermediates']
    steps = []

    # Bước 1: Thông báo về tính đối xứng và ma trận M
    steps.append({"message": f"<b>Bước 1:</b> {result['transformation_message']}"})
    if result['intermediates']['M'] is not None:
        steps[-1]['M'] = inter['M'].tolist()

    # Bước 2: Phân rã Cholesky
    steps.append({
        "message": "<b>Bước 2:</b> Phân rã Cholesky M = UᵀU.",
        "Ut": inter['Ut'].tolist(),
        "U": inter['U'].tolist()
    })

    # Bước 3: Tính U⁻¹
    steps.append({
        "message": "<b>Bước 3:</b> Tính U⁻¹ bằng cách giải hệ UX = I.",
        "matrix": inter['U_inv'].tolist(),
        "num_vars": result['num_vars']
    })

    # Bước 4: Tính M⁻¹
    steps.append({
        "message": "<b>Bước 4:</b> Tính M⁻¹ = U⁻¹(U⁻¹)ᵀ.",
        "matrix": inter['M_inv'].tolist(),
        "num_vars": result['num_vars']
    })

    # Bước 5 (nếu cần): Tính A⁻¹ từ M⁻¹
    if not result['is_symmetric']:
        steps.append({
            "message": "<b>Bước 5:</b> Tính A⁺ = M⁻¹Aᵀ.",
            "matrix": result['inverse'].tolist(),
            "num_vars": result['num_vars']
        })

    return {
        "method": "Ma trận nghịch đảo (Cholesky)",
        "status": "success",
        "message": result['final_message'],
        "inverse": result['inverse'].tolist(),
        "steps": steps
    }

def format_bordering_inverse_result(result):
    """
    Định dạng kết quả tính ma trận nghịch đảo bằng phương pháp viền quanh.
    """
    steps_formatted = []
    for step in result['steps']:
        k = step['k']
        if k == 1:
            message = f"<b>Bước 1:</b> Nghịch đảo của ma trận con cấp 1 A₁ = [[{step['A_k']:.4f}]]"
        else:
            message = f"<b>Bước {k}:</b> Tính nghịch đảo cho ma trận con cấp {k}. (θ ≈ {step['theta']:.4f})"
        
        steps_formatted.append({
            "message": message,
            "matrix": step['inv_A_k'].tolist()
        })
    
    # Thêm bước kiểm tra cuối cùng
    steps_formatted.append({
        "message": "<b>Kiểm tra:</b> A * A⁻¹ ≈ I",
        "matrix": result['check'].tolist()
    })

    return {
        "method": "Ma trận nghịch đảo (Viền quanh)",
        "status": "success",
        "message": "Tính ma trận nghịch đảo thành công bằng phương pháp viền quanh.",
        "inverse": result['inverse'].tolist(),
        "steps": steps_formatted
    }

def format_jacobi_result(result):
    """
    Định dạng kết quả từ phương pháp lặp Jacobi.
    """
    if result.get('status') != 'success':
        return {"error": result.get('error', 'Lỗi không xác định')}

    dominance_msg = "hàng" if result['is_row_dominant'] else "cột"
    norm_symbol = "∞" if result['norm_used'] == "infinity" else "1"
    
    table = []
    for row in result['iterations_data']:
        table.append({
            "k": row['k'],
            "x_k": row['x_k'].tolist(),
            "error": row['error'],
            "diff_norm": row['diff_norm']
        })

    return {
        "method": "Lặp Jacobi",
        "status": "success",
        "message": f"Hội tụ sau {result['iterations']} lần lặp.",
        "solution": result['solution'].tolist(),
        "convergence_info": {
            "dominance_type": f"Ma trận chéo trội {dominance_msg}",
            "norm_used": f"Sử dụng chuẩn {norm_symbol}",
            "contraction_coefficient": result['contraction_coefficient']
        },
        "iteration_matrix": {
            "B": result['matrix_B'].tolist(),
            "d": result['vector_d'].tolist()
        },
        "steps": [{"table": table}]
    }

def format_gauss_seidel_result(result):
    # Định dạng kết quả từ phương pháp lặp Gauss-Seidel.
    if result.get('status') != 'success':
        return {"error": result.get('error', 'Lỗi không xác định')}

    dominance_msg = "hàng" if result['is_row_dominant'] else "cột"
    norm_symbol = "∞" if result['norm_used'] == "infinity" else "1"
    
    table = [{"k": row['k'], "x_k": row['x_k'].tolist(), "error": row['error'], "diff_norm": row['diff_norm']} for row in result['iterations_data']]

    return {
        "method": "Lặp Gauss-Seidel",
        "status": "success",
        "message": f"Hội tụ sau {result['iterations']} lần lặp.",
        "solution": result['solution'].tolist(),
        "convergence_info": {
            "dominance_type": f"Ma trận chéo trội {dominance_msg}",
            "norm_used": f"Sử dụng chuẩn {norm_symbol}",
            "coeff_q": result['coeff_q'],
            "coeff_s": result['coeff_s']
        },
        "steps": [{"table": table}]
    }

def format_simple_iteration_result(result):
    # Định dạng kết quả từ phương pháp lặp đơn.
    if result.get('status') != 'success':
        return {"error": result.get('error', 'Lỗi không xác định')}

    norm_symbol = "∞" if result['norm_used'] == 'inf' else "1"
    
    table = [{"k": row['k'], "x_k": row['x_k'].tolist(), "error": row['error']} for row in result['iterations_data']]

    return {
        "method": "Lặp Đơn",
        "status": "success",
        "message": f"Hội tụ sau {result['iterations']} lần lặp.",
        "solution": result['solution'].tolist(),
        "convergence_info": {
            "norm_used": f"Sử dụng chuẩn {norm_symbol}",
            "contraction_coefficient": result['norm_B'],
            "warning_message": result['warning_message'],
            "stopping_threshold": result.get('stopping_threshold')
        },
        "steps": [{"table": table}]
    }

def format_inverse_jacobi_result(result):
    if result.get('status') != 'success':
        return {"error": result.get('error', 'Lỗi không xác định')}

    dominance_msg = "hàng" if result['is_row_dominant'] else "cột"
    norm_symbol = "∞" if result['norm_used'] == "infinity" else "1"
    x0_label = "Aᵀ / ||A||₂²" if result['x0_method'] == 'method1' else "Aᵀ / (||A||₁·||A||∞)"

    table = []
    for row in result['iterations_data']:
        table.append({
            "k": row['k'],
            "x_k": row['x_k'].tolist(),
            "error": row['diff_norm'], 
            "estimated_error": row['error']
        })

    return {
        "method": "Lặp Jacobi - Nghịch Đảo",
        "status": "success",
        "message": f"Hội tụ sau {result['iterations']} lần lặp.",
        "inverse": result['inverse'].tolist(),
        "check_matrix": result['check_matrix'].tolist(),
        "convergence_info": {
            "dominance_type": f"Ma trận chéo trội {dominance_msg}",
            "norm_used": f"Sử dụng chuẩn {norm_symbol}",
            "contraction_coefficient": result['contraction_coefficient'],
            "x0_label": f"X₀ = {x0_label}"
        },
        "initial_matrix": result['initial_matrix'].tolist(),
        "steps": [{"table": table}]
    }

def format_inverse_newton_result(result):
    if result.get('status') != 'success':
        return {"error": result.get('error', 'Lỗi không xác định')}

    table = []
    for row in result['iterations_data']:
        table.append({
            "k": row['k'],
            "x_k": row['x_k'].tolist(),
            "error": row['diff_norm'], 
            "estimated_error": row['estimated_error']
        })

    return {
        "method": "Lặp tựa Newton - Nghịch Đảo",
        "status": "success",
        "message": f"Hội tụ sau {result['iterations']} lần lặp.",
        "inverse": result['inverse'].tolist(),
        "check_matrix": result['check_matrix'].tolist(),
        "convergence_info": {
            "norm_used": "Sử dụng chuẩn 2", # Newton luôn dùng chuẩn 2
            "contraction_coefficient": result['contraction_coefficient'],
            "x0_label": result['x0_label']
        },
        "initial_matrix": result['initial_matrix'].tolist(),
        "steps": [{"table": table}]
    }

def format_inverse_gauss_seidel_result(result):
    if result.get('status') != 'success':
        return {"error": result.get('error', 'Lỗi không xác định')}

    dominance_msg = "hàng" if result['is_row_dominant'] else "cột"
    norm_symbol = "∞" if result['norm_used'] == "infinity" else "1"
    x0_label = "Aᵀ / ||A||₂²" if result['x0_method'] == 'method1' else "Aᵀ / (||A||₁·||A||∞)"

    table = []
    for row in result['iterations_data']:
        table.append({
            "k": row['k'],
            "x_k": row['x_k'].tolist(),
            "error": row['diff_norm'], 
            "estimated_error": row['error']
        })

    return {
        "method": "Lặp Gauss-Seidel - Nghịch Đảo",
        "status": "success",
        "message": f"Hội tụ sau {result['iterations']} lần lặp.",
        "inverse": result['inverse'].tolist(),
        "check_matrix": result['check_matrix'].tolist(),
        "convergence_info": {
            "dominance_type": f"Ma trận chéo trội {dominance_msg}",
            "norm_used": f"Sử dụng chuẩn {norm_symbol}",
            "coeff_q": result['coeff_q'],
            "coeff_s": result['coeff_s'],
            "x0_label": f"X₀ = {x0_label}"
        },
        "initial_matrix": result['initial_matrix'].tolist(),
        "steps": [{"table": table}]
    }

def format_svd_result(result, original_shape):
    if result.get('status') != 'success':
        return result

    m, n = original_shape
    U, s, Vt = result['U'], result['Sigma_diag'], result['Vt']
    
    # Tạo ma trận Sigma đầy đủ
    Sigma = np.zeros((U.shape[1], Vt.shape[0]))
    np.fill_diagonal(Sigma, s)
    
    # Xử lý các bước trung gian (nếu có)
    intermediate_steps = result.get('intermediate_steps')
    if intermediate_steps and 'steps' in intermediate_steps:
        for step in intermediate_steps['steps']:
            step['matrix_before_deflation'] = step['matrix_before_deflation'].tolist()
            step['matrix_after_deflation'] = step['matrix_after_deflation'].tolist()
            step['eigenvector'] = step['eigenvector'].tolist()
            step['y_steps'] = [y.tolist() for y in step['y_steps']]
        intermediate_steps['original_matrix'] = intermediate_steps['original_matrix'].tolist()

    return {
        "method": result['method'],
        "status": "success",
        "U": U.tolist(),
        "Sigma": Sigma.tolist(),
        "Vt": Vt.tolist(),
        "Sigma_diag": s.tolist(),
        "intermediate_steps": intermediate_steps
    }

def format_danilevsky_result(result, A):
    if result.get('status') != 'success':
        return result

    # Hàm nội bộ để định dạng số phức
    def format_complex(c):
        if abs(np.imag(c)) < 1e-9:
            return np.real(c)
        return {'real': np.real(c), 'imag': np.imag(c)}

    # Hàm nội bộ để định dạng và chuẩn hóa vector
    def format_vector_for_json(v):
        max_abs_idx = np.argmax(np.abs(v))
        if np.abs(v[max_abs_idx, 0]) > 1e-9:
            v = v / v[max_abs_idx, 0]
        return [[format_complex(c)] for c in v.flatten()]

    # Định dạng các bước biến đổi
    for step in result['steps']:
        step['matrix'] = [[format_complex(c) for c in row] for row in step['matrix'].tolist()]
        if 'M' in step:
            step['M'] = [[format_complex(c) for c in row] for row in step['M'].tolist()]
        if 'M_inv' in step:
            step['M_inv'] = [[format_complex(c) for c in row] for row in step['M_inv'].tolist()]
    
    # Tính toán kiểm tra và tạo cấu trúc dữ liệu mới
    eigen_pairs = []
    raw_eigenvalues = result['eigenvalues']
    raw_eigenvectors = result['eigenvectors']

    for i in range(len(raw_eigenvalues)):
        lambda_val = raw_eigenvalues[i]
        v = raw_eigenvectors[i]

        # Thực hiện phép kiểm tra
        Av = A.astype(complex) @ v
        lambda_v = lambda_val * v

        eigen_pairs.append({
            'lambda': format_complex(lambda_val),
            'v': format_vector_for_json(v),
            'Av_check': format_vector_for_json(Av),
            'lambda_v_check': format_vector_for_json(lambda_v)
        })

    return {
        "method": "Danilevsky",
        "status": "success",
        "char_poly": [format_complex(c) for c in result['char_poly']],
        "eigen_pairs": eigen_pairs, # Dữ liệu được cấu trúc lại
        "steps": result['steps']
    }

def format_power_method_result(result, A):
    if result.get('status') == 'success_zero':
        return {
            "method": "Power Method", "status": "success",
            "message": "Vector lặp tiến về 0, GTR trội là 0.",
            "eigen_pairs": [{'lambda': 0.0, 'v': result['eigenvector'].tolist()}]
        }

    if result.get('status') != 'success':
        return result

    def format_vector_for_json(v):
        max_abs_idx = np.argmax(np.abs(v))
        if np.abs(v[max_abs_idx, 0]) > 1e-9:
            v = v / v[max_abs_idx, 0]
        return [[c] for c in v.flatten().tolist()]

    eigen_pairs = []
    if 'eigen_pairs' in result: # Deflation case
        method = f"Power Method & Deflation ({len(result['eigen_pairs'])} GTR)"
        for pair in result['eigen_pairs']:
            lambda_val = pair['eigenvalue']
            v = pair['eigenvector']
            Av = A @ v
            lambda_v = lambda_val * v
            eigen_pairs.append({
                'lambda': lambda_val,
                'v': format_vector_for_json(v),
                'Av_check': format_vector_for_json(Av),
                'lambda_v_check': format_vector_for_json(lambda_v)
            })
    else: # Single case
        method = "Power Method (GTR Trội)"
        lambda_val = result['eigenvalue']
        v = result['eigenvector']
        Av = A @ v
        lambda_v = lambda_val * v
        eigen_pairs.append({
            'lambda': lambda_val,
            'v': format_vector_for_json(v),
            'Av_check': format_vector_for_json(Av),
            'lambda_v_check': format_vector_for_json(lambda_v)
        })

    # Sửa đổi: Đảm bảo TẤT CẢ ndarray được chuyển thành list
    if 'steps' in result:
        for step in result['steps']:
            if 'iteration_details' in step: # Deflation
                step['desc'] = f"<b>Tìm trị riêng thứ {step['eigenvalue_index']}:</b> Ma trận trước khi xuống thang"
                # Chuyển đổi ma trận sang list
                step['matrix'] = step['matrix_before_deflation'].tolist()
                del step['matrix_before_deflation']
                
                # Chuyển đổi các ndarray bên trong chi tiết lặp
                for detail in step['iteration_details']:
                    detail['x_k'] = detail['x_k'].tolist()
                    detail['Ax_k'] = detail['Ax_k'].tolist()
            else: # Single
                step['desc'] = f"<b>Bước {step['k']}:</b> Lặp lần thứ {step['k']}"
                # Chuyển đổi các vector sang list
                step['x_k'] = step['x_k'].tolist()
                step['Ax_k'] = step['Ax_k'].tolist()
                # lambda_k đã là float, không cần chuyển đổi

    return {
        "method": method,
        "status": "success",
        "eigen_pairs": eigen_pairs,
        "steps": result.get('steps')
    }