# backend/api_formatters/linear_algebra.py
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