# backend/routes/linear_algebra_routes.py
from flask import Blueprint, request, jsonify
import numpy as np
from backend.numerical_methods.linear_algebra.direct.gauss_elimination import gauss_elimination
from backend.api_formatters.linear_algebra import format_gauss_elimination_result
from backend.utils.helpers import parse_matrix_from_string
from backend.numerical_methods.linear_algebra.direct.gauss_jordan import gauss_jordan
from backend.api_formatters.linear_algebra import format_gauss_jordan_result

linear_algebra_bp = Blueprint('linear_algebra', __name__, url_prefix='/api/linear-algebra')

@linear_algebra_bp.route('/solve/gauss', methods=['POST'])
def solve_gauss():
    try:
        data = request.json
        
        matrix_a_str = data.get('matrix_a')
        matrix_b_str = data.get('matrix_b')
        zero_tolerance_str = data.get('zero_tolerance', '1e-15')

        try:
            zero_tolerance = float(zero_tolerance_str)
        except (ValueError, TypeError):
            zero_tolerance = 1e-15

        if not matrix_a_str or not matrix_b_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ ma trận A và vector b."}), 400

        # Chuyển đổi chuỗi thành ma trận NumPy
        A = parse_matrix_from_string(matrix_a_str)
        b = parse_matrix_from_string(matrix_b_str)

        # Kiểm tra xem A và B có cùng số hàng không
        if A.shape[0] != b.shape[0]:
             return jsonify({"error": f"Lỗi kích thước: Ma trận A có {A.shape[0]} hàng, nhưng ma trận B có {b.shape[0]} hàng. Chúng phải bằng nhau."}), 400
        
        # --- ĐÃ XÓA BỎ ĐOẠN KIỂM TRA MA TRẬN VUÔNG Ở ĐÂY ---

        # Truyền giá trị tolerance vào hàm thuật toán
        result = gauss_elimination(A, b, tol=zero_tolerance)
        
        # Định dạng kết quả và trả về
        formatted_result = format_gauss_elimination_result(result)
        return jsonify(formatted_result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500

@linear_algebra_bp.route('/solve/gauss-jordan', methods=['POST'])
def solve_gauss_jordan_route():
    try:
        data = request.json
        matrix_a_str = data.get('matrix_a')
        matrix_b_str = data.get('matrix_b')
        zero_tolerance_str = data.get('zero_tolerance', '1e-15')
        
        try:
            zero_tolerance = float(zero_tolerance_str)
        except (ValueError, TypeError):
            zero_tolerance = 1e-15

        if not matrix_a_str or not matrix_b_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ ma trận A và vector b."}), 400

        A = parse_matrix_from_string(matrix_a_str)
        b = parse_matrix_from_string(matrix_b_str)

        if A.shape[0] != b.shape[0]:
             return jsonify({"error": f"Lỗi kích thước: Ma trận A có {A.shape[0]} hàng, nhưng B có {b.shape[0]} hàng. Chúng phải bằng nhau."}), 400

        result = gauss_jordan(A, b, tol=zero_tolerance)
        formatted_result = format_gauss_jordan_result(result)
        return jsonify(formatted_result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500