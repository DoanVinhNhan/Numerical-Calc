# backend/routes/horner_routes.py
from backend.numerical_methods.horner_table.all_derivatives import all_derivatives
from flask import Blueprint, request, jsonify
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.api_formatters.horner_table import format_all_derivatives_result, format_synthetic_division_result
from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
from backend.api_formatters.horner_table import format_reverse_horner_result
from backend.numerical_methods.horner_table.w_function import calculate_w_function
from backend.api_formatters.horner_table import format_w_function_result
from backend.numerical_methods.horner_table.change_variables import change_variables
from backend.api_formatters.horner_table import format_change_variables_result
import traceback

horner_bp = Blueprint('horner', __name__, url_prefix='/api/horner')

@horner_bp.route('/synthetic-division', methods=['POST'])
def synthetic_division_route():
    try:
        data = request.json
        coeffs_str = data.get('coeffs', '').split()
        if not coeffs_str:
            return jsonify({"error": "Vui lòng nhập các hệ số của đa thức."}), 400
            
        coeffs = [float(c) for c in coeffs_str]
        root = float(data.get('root'))

        result = synthetic_division(coeffs, root)
        
        # Thêm dữ liệu gốc vào kết quả để formatter sử dụng
        result['coeffs'] = coeffs
        result['root'] = root

        formatted_result = format_synthetic_division_result(result)
        
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi không xác định: {traceback.format_exc()}"}), 500

@horner_bp.route('/all-derivatives', methods=['POST'])
def all_derivatives_route():
    try:
        data = request.json
        coeffs_str = data.get('coeffs', '').split()
        if not coeffs_str:
            return jsonify({"error": "Vui lòng nhập các hệ số của đa thức."}), 400

        coeffs = [float(c) for c in coeffs_str]
        root = float(data.get('root'))
        # Lấy giá trị 'order' từ request
        order_str = data.get('order')

        # Kiểm tra nếu chuỗi rỗng hoặc không tồn tại, thì đặt giá trị mặc định
        if not order_str:
            order = len(coeffs) - 1  # Mặc định là bậc của đa thức
        else:
            order = int(order_str)

        result = all_derivatives(coeffs, root, order)
        
        # Thêm thông tin để formatter sử dụng
        result['coeffs'] = coeffs
        result['root'] = root
        result['order'] = order


        formatted_result = format_all_derivatives_result(result)

        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi không xác định: {traceback.format_exc()}"}), 500

@horner_bp.route('/reverse-horner', methods=['POST'])
def reverse_horner_route():
    try:
        data = request.json
        coeffs_str = data.get('coeffs', '').split()
        if not coeffs_str:
            return jsonify({"error": "Vui lòng nhập các hệ số của đa thức."}), 400

        coeffs = [float(c) for c in coeffs_str]
        root = float(data.get('root'))

        result = reverse_horner(coeffs, root)

        # Thêm dữ liệu gốc để formatter sử dụng
        result['original_coeffs'] = coeffs
        result['root'] = root

        formatted_result = format_reverse_horner_result(result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi không xác định: {traceback.format_exc()}"}), 500
    
@horner_bp.route('/w-function', methods=['POST'])
def w_function_route():
    try:
        data = request.json
        roots_str = data.get('roots', '').split()
        if not roots_str:
            return jsonify({"error": "Vui lòng nhập các nghiệm x_i."}), 400

        roots = [float(r) for r in roots_str]
        
        result = calculate_w_function(roots)
        
        formatted_result = format_w_function_result(result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi không xác định: {traceback.format_exc()}"}), 500
    
@horner_bp.route('/change-variables', methods=['POST'])
def change_variables_route():
    try:
        data = request.json
        coeffs_str = data.get('coeffs', '').split()
        if not coeffs_str:
            return jsonify({"error": "Vui lòng nhập các hệ số của đa thức."}), 400

        coeffs = [float(c) for c in coeffs_str]
        a = float(data.get('a'))
        b = float(data.get('b'))

        result = change_variables(coeffs, a, b)
        
        # Thêm thông tin để formatter sử dụng
        result['original_coeffs'] = coeffs
        result['a'] = a
        result['b'] = b

        formatted_result = format_change_variables_result(result)

        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi không xác định: {traceback.format_exc()}"}), 500