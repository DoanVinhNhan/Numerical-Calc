# backend/routes/horner_routes.py
from backend.numerical_methods.horner_table.all_derivatives import all_derivatives
from flask import Blueprint, request, jsonify
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.api_formatters.horner_table import format_all_derivatives_result, format_synthetic_division_result
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
        order = int(data.get('order', 0))

        result = all_derivatives(coeffs, root, order)

        formatted_result = format_all_derivatives_result(result)

        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi không xác định: {traceback.format_exc()}"}), 500