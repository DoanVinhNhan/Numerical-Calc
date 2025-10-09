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