# backend/api_formatters/linear_algebra.py

def format_gauss_elimination_result(result):
    """
    Định dạng kết quả từ phương pháp khử Gauss để trả về qua API.
    Tạo ra các thông báo tường minh cho frontend.
    """
    # Chuyển đổi các bước khử xuôi thành thông báo
    steps_formatted = []
    step_counter = 1
    for step_data in result['steps']:
        message = ""
        if step_data['type'] == 'pivot':
            message = f"<b>Bước {step_counter}:</b> Hoán vị hàng {step_data['to_row'] + 1} và {step_data['from_row'] + 1} để đưa phần tử trụ lớn nhất lên trên."
        elif step_data['type'] == 'elimination':
            message = f"<b>Bước {step_counter}:</b> Dùng hàng {step_data['pivot_row']+1} để khử các phần tử trong cột {step_data['pivot_col']+1}."
        
        steps_formatted.append({
            "message": message,
            "matrix": step_data['matrix'].tolist()
        })
        step_counter += 1

    # Xử lý các trạng thái kết quả khác nhau
    if result['status'] == 'no_solution':
        return {
            "method": "Khử Gauss",
            "status": "no_solution",
            "message": "Hệ phương trình vô nghiệm (Hạng(A) < Hạng([A|B])).",
            "steps": steps_formatted
        }
        
    elif result['status'] == 'infinite_solutions':
        return {
            "method": "Khử Gauss",
            "status": "infinite_solutions",
            "message": f"Hệ có vô số nghiệm (Hạng = {result['rank']} < Số ẩn = {result['num_vars']}).",
            "steps": steps_formatted,
            "general_solution": {
                "particular_solution": result['particular_solution'].tolist(),
                "null_space_vectors": result['null_space_vectors'].tolist()
            }
        }
        
    elif result['status'] == 'unique_solution':
        # Chuyển đổi các bước thế ngược thành thông báo
        backward_steps_formatted = []
        for bs_step in result['backward_steps']:
            backward_steps_formatted.append({
                "message": f"Tính toán cho biến x<sub>{bs_step['row']+1}</sub>.",
                "solution_so_far": bs_step['solution_so_far'].tolist()
            })
            
        return {
            "method": "Khử Gauss",
            "status": "unique_solution",
            "message": "Hệ phương trình có nghiệm duy nhất.",
            "solution": result['solution'].tolist(),
            "steps": steps_formatted,
            "backward_steps": backward_steps_formatted
        }
        
    # Trường hợp lỗi không mong muốn
    return {"error": "Đã xảy ra lỗi không xác định trong quá trình định dạng kết quả."}