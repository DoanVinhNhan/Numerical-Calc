# backend/routes/linear_algebra_routes.py
from flask import Blueprint, request, jsonify
import numpy as np
from backend.numerical_methods.linear_algebra.direct.gauss_elimination import gauss_elimination
from backend.api_formatters.linear_algebra import format_gauss_elimination_result
from backend.utils.helpers import parse_matrix_from_string

linear_algebra_bp = Blueprint('linear_algebra', __name__, url_prefix='/api/linear-algebra')

@linear_algebra_bp.route('/solve/gauss', methods=['POST'])
def solve_gauss():
    try:
        data = request.json
        
        # Lấy chuỗi ma trận từ request
        matrix_a_str = data.get('matrix_a')
        matrix_b_str = data.get('matrix_b')

        # Nhận giá trị tolerance từ frontend
        # Dùng giá trị mặc định '1e-15' nếu frontend không gửi
        zero_tolerance_str = data.get('zero_tolerance', '1e-15')
        try:
            # Chuyển đổi chuỗi (ví dụ: "1e-15") thành số float
            zero_tolerance = float(zero_tolerance_str)
        except (ValueError, TypeError):
            # Nếu có lỗi, quay về giá trị mặc định an toàn
            zero_tolerance = 1e-15

        if not matrix_a_str or not matrix_b_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ ma trận A và vector b."}), 400

        # Chuyển đổi chuỗi thành ma trận NumPy
        A = parse_matrix_from_string(matrix_a_str)
        b = parse_matrix_from_string(matrix_b_str)

        # Kiểm tra kích thước ma trận
        if A.shape[0] != b.shape[0]:
             return jsonify({"error": "Số hàng của ma trận A và vector b phải bằng nhau."}), 400
        if A.shape[0] != A.shape[1]:
            return jsonify({"error": "Ma trận A phải là ma trận vuông."}), 400

        # Truyền giá trị tolerance vào hàm thuật toán
        result = gauss_elimination(A, b, tol=zero_tolerance)
        
        # Định dạng kết quả và trả về
        formatted_result = format_gauss_elimination_result(result)
        return jsonify(formatted_result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500