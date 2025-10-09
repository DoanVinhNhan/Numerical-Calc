# backend/routes/linear_algebra_routes.py
from flask import Blueprint, request, jsonify
import numpy as np
from backend.numerical_methods.linear_algebra.direct.gauss_elimination import gauss_elimination
from backend.api_formatters.linear_algebra import format_gauss_elimination_result
from backend.utils.helpers import parse_matrix_from_string
from backend.numerical_methods.linear_algebra.direct.gauss_jordan import gauss_jordan
from backend.api_formatters.linear_algebra import format_gauss_jordan_result
from backend.numerical_methods.linear_algebra.direct.lu_decomposition import solve_lu
from backend.api_formatters.linear_algebra import format_lu_result
from backend.numerical_methods.linear_algebra.direct.cholesky import solve_cholesky
from backend.api_formatters.linear_algebra import format_cholesky_result
from backend.numerical_methods.linear_algebra.inverse.gauss_jordan_inverse import gauss_jordan_inverse
from backend.api_formatters.linear_algebra import format_inverse_gauss_jordan_result


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

@linear_algebra_bp.route('/solve/cholesky', methods=['POST'])
def solve_cholesky_route():
    try:
        data = request.json
        
        # 1. Lấy dữ liệu từ request JSON
        matrix_a_str = data.get('matrix_a')
        matrix_b_str = data.get('matrix_b')
        zero_tolerance_str = data.get('zero_tolerance', '1e-15')

        # 2. Xử lý ngưỡng làm tròn (tolerance)
        try:
            zero_tolerance = float(zero_tolerance_str)
        except (ValueError, TypeError):
            # Nếu có lỗi, quay về giá trị mặc định an toàn
            zero_tolerance = 1e-15

        # 3. Kiểm tra đầu vào cơ bản
        if not matrix_a_str or not matrix_b_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ ma trận A và vector b."}), 400

        # 4. Phân tích chuỗi thành ma trận NumPy
        A = parse_matrix_from_string(matrix_a_str)
        b = parse_matrix_from_string(matrix_b_str)

        # 5. Kiểm tra tính hợp lệ của kích thước ma trận
        if A.shape[0] != b.shape[0]:
             return jsonify({"error": f"Lỗi kích thước: Ma trận A có {A.shape[0]} hàng, nhưng ma trận B có {b.shape[0]} hàng. Chúng phải bằng nhau."}), 400

        # 6. Gọi hàm thuật toán chính
        result = solve_cholesky(A, b, tol=zero_tolerance)
        
        # 7. Định dạng kết quả để trả về cho frontend
        formatted_result = format_cholesky_result(result)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        # Bắt các lỗi tính toán hoặc định dạng cụ thể và trả về lỗi 400 (Bad Request)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Bắt các lỗi không mong muốn khác và trả về lỗi 500 (Internal Server Error)
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn trên máy chủ: {str(e)}"}), 500

@linear_algebra_bp.route('/solve/lu', methods=['POST'])
def solve_lu_route():
    try:
        data = request.json
        
        # 1. Lấy dữ liệu từ request JSON
        matrix_a_str = data.get('matrix_a')
        matrix_b_str = data.get('matrix_b')
        zero_tolerance_str = data.get('zero_tolerance', '1e-15')

        # 2. Xử lý ngưỡng làm tròn (tolerance)
        try:
            zero_tolerance = float(zero_tolerance_str)
        except (ValueError, TypeError):
            # Nếu có lỗi, quay về giá trị mặc định an toàn
            zero_tolerance = 1e-15

        # 3. Kiểm tra đầu vào cơ bản
        if not matrix_a_str or not matrix_b_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ ma trận A và vector b."}), 400

        # 4. Phân tích chuỗi thành ma trận NumPy
        A = parse_matrix_from_string(matrix_a_str)
        b = parse_matrix_from_string(matrix_b_str)

        # 5. Kiểm tra tính hợp lệ của kích thước ma trận
        if A.shape[0] != b.shape[0]:
             return jsonify({"error": f"Lỗi kích thước: Ma trận A có {A.shape[0]} hàng, nhưng ma trận B có {b.shape[0]} hàng. Chúng phải bằng nhau."}), 400

        # 6. Gọi hàm thuật toán chính
        result = solve_lu(A, b, tol=zero_tolerance)
        
        # 7. Định dạng kết quả để trả về cho frontend
        formatted_result = format_lu_result(result)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        # Bắt các lỗi tính toán hoặc định dạng cụ thể và trả về lỗi 400 (Bad Request)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Bắt các lỗi không mong muốn khác và trả về lỗi 500 (Internal Server Error)
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn trên máy chủ: {str(e)}"}), 500

@linear_algebra_bp.route('/inverse/gauss-jordan', methods=['POST'])
def inverse_gauss_jordan_route():
    """
    Route để tính ma trận nghịch đảo bằng phương pháp Gauss-Jordan.
    """
    try:
        data = request.json
        matrix_a_str = data.get('matrix_a')
        zero_tolerance_str = data.get('zero_tolerance', '1e-15')
        
        # Xử lý tolerance
        try:
            zero_tolerance = float(zero_tolerance_str)
        except (ValueError, TypeError):
            zero_tolerance = 1e-15

        if not matrix_a_str:
            return jsonify({"error": "Vui lòng nhập ma trận A."}), 400

        # Chuyển đổi chuỗi thành ma trận NumPy
        A = parse_matrix_from_string(matrix_a_str)

        # Kiểm tra ma trận vuông
        if A.shape[0] != A.shape[1]:
            return jsonify({"error": f"Ma trận A phải là ma trận vuông để tính nghịch đảo. Ma trận hiện tại có kích thước {A.shape[0]}x{A.shape[1]}."}), 400

        # Gọi hàm tính ma trận nghịch đảo
        result = gauss_jordan_inverse(A, tol=zero_tolerance)
        
        # Định dạng kết quả và trả về
        formatted_result = format_inverse_gauss_jordan_result(result)
        return jsonify(formatted_result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500
