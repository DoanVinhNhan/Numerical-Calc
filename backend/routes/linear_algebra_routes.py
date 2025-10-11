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
from backend.numerical_methods.linear_algebra.inverse.lu_inverse import lu_inverse
from backend.api_formatters.linear_algebra import format_lu_inverse_result
from backend.numerical_methods.linear_algebra.inverse.cholesky_inverse import cholesky_inverse
from backend.api_formatters.linear_algebra import format_cholesky_inverse_result
from backend.numerical_methods.linear_algebra.inverse.bordering import bordering_inverse
from backend.api_formatters.linear_algebra import format_bordering_inverse_result
from backend.numerical_methods.linear_algebra.iterative.jacobi import jacobi
from backend.api_formatters.linear_algebra import format_jacobi_result
from backend.numerical_methods.linear_algebra.iterative.gauss_seidel import gauss_seidel
from backend.api_formatters.linear_algebra import format_gauss_seidel_result
from backend.numerical_methods.linear_algebra.iterative.simple_iteration import simple_iteration
from backend.api_formatters.linear_algebra import format_simple_iteration_result
from backend.numerical_methods.linear_algebra.inverse.jacobi_inverse import jacobi_inverse
from backend.api_formatters.linear_algebra import format_inverse_jacobi_result
from backend.numerical_methods.linear_algebra.inverse.newton_inverse import newton_inverse
from backend.api_formatters.linear_algebra import format_inverse_newton_result
from backend.numerical_methods.linear_algebra.inverse.gauss_seidel_inverse import gauss_seidel_inverse
from backend.api_formatters.linear_algebra import format_inverse_gauss_seidel_result
from backend.numerical_methods.linear_algebra.eigen.svd import svd_numpy, svd_power_deflation
from backend.api_formatters.linear_algebra import format_svd_result
from backend.numerical_methods.linear_algebra.eigen.danilevsky import danilevsky_algorithm
from backend.api_formatters.linear_algebra import format_danilevsky_result
from backend.numerical_methods.linear_algebra.eigen.power_method import power_method_single, power_method_deflation
from backend.api_formatters.linear_algebra import format_power_method_result
from backend.numerical_methods.linear_algebra.eigen.svd import calculate_svd_approximation # THÊM DÒNG NÀY
from backend.api_formatters.linear_algebra import format_svd_approximation_result # THÊM DÒNG NÀY


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

@linear_algebra_bp.route('/inverse/lu', methods=['POST'])
def inverse_lu_route():
    """
    Route để tính ma trận nghịch đảo bằng phương pháp phân rã LU.
    """
    try:
        data = request.json
        matrix_a_str = data.get('matrix_a')
        zero_tolerance_str = data.get('zero_tolerance', '1e-15')
        
        try:
            zero_tolerance = float(zero_tolerance_str)
        except (ValueError, TypeError):
            zero_tolerance = 1e-15

        if not matrix_a_str:
            return jsonify({"error": "Vui lòng nhập ma trận A."}), 400

        A = parse_matrix_from_string(matrix_a_str)

        if A.shape[0] != A.shape[1]:
            return jsonify({"error": f"Ma trận A phải là ma trận vuông. Kích thước hiện tại là {A.shape[0]}x{A.shape[1]}."}), 400

        result = lu_inverse(A, tol=zero_tolerance)
        
        formatted_result = format_lu_inverse_result(result)
        return jsonify(formatted_result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500

@linear_algebra_bp.route('/inverse/cholesky', methods=['POST'])
def inverse_cholesky_route():
    """
    Route để tính ma trận nghịch đảo bằng phương pháp Cholesky.
    """
    try:
        data = request.json
        matrix_a_str = data.get('matrix_a')
        zero_tolerance_str = data.get('zero_tolerance', '1e-15')
        
        try:
            zero_tolerance = float(zero_tolerance_str)
        except (ValueError, TypeError):
            zero_tolerance = 1e-15

        if not matrix_a_str:
            return jsonify({"error": "Vui lòng nhập ma trận A."}), 400

        A = parse_matrix_from_string(matrix_a_str)

        if A.shape[0] != A.shape[1]:
            return jsonify({"error": f"Ma trận A phải là ma trận vuông. Kích thước hiện tại là {A.shape[0]}x{A.shape[1]}."}), 400

        result = cholesky_inverse(A, tol=zero_tolerance)
        
        formatted_result = format_cholesky_inverse_result(result)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500
    
@linear_algebra_bp.route('/inverse/bordering', methods=['POST'])
def inverse_bordering_route():
    """
    Route để tính ma trận nghịch đảo bằng phương pháp viền quanh.
    """
    try:
        data = request.json
        matrix_a_str = data.get('matrix_a')
        zero_tolerance_str = data.get('zero_tolerance', '1e-15')
        
        try:
            zero_tolerance = float(zero_tolerance_str)
        except (ValueError, TypeError):
            zero_tolerance = 1e-15

        if not matrix_a_str:
            return jsonify({"error": "Vui lòng nhập ma trận A."}), 400

        A = parse_matrix_from_string(matrix_a_str)

        result = bordering_inverse(A, tol=zero_tolerance)
        
        formatted_result = format_bordering_inverse_result(result)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500
    
@linear_algebra_bp.route('/solve/jacobi', methods=['POST'])
def solve_jacobi_route():
    try:
        data = request.json
        A = parse_matrix_from_string(data.get('matrix_a'))
        b = parse_matrix_from_string(data.get('matrix_b'))
        x0 = parse_matrix_from_string(data.get('x0'))
        
        tol = float(data.get('tolerance', 1e-5))
        max_iter = int(data.get('max_iter', 100))
        
        result = jacobi(A, b, x0, tol=tol, max_iter=max_iter)
        formatted_result = format_jacobi_result(result)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500

@linear_algebra_bp.route('/solve/gauss-seidel', methods=['POST'])
def solve_gauss_seidel_route():
    try:
        data = request.json
        A = parse_matrix_from_string(data.get('matrix_a'))
        b = parse_matrix_from_string(data.get('matrix_b'))
        x0 = parse_matrix_from_string(data.get('x0'))
        
        tol = float(data.get('tolerance', 1e-5))
        max_iter = int(data.get('max_iter', 100))
        
        result = gauss_seidel(A, b, x0, tol=tol, max_iter=max_iter)
        formatted_result = format_gauss_seidel_result(result)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500

@linear_algebra_bp.route('/solve/simple-iteration', methods=['POST'])
def solve_simple_iteration_route():
    try:
        data = request.json
        B = parse_matrix_from_string(data.get('matrix_b')) # Lưu ý: matrix_b từ frontend là B
        d = parse_matrix_from_string(data.get('matrix_d'))
        x0_str = data.get('x0')
        
        if not x0_str or not x0_str.strip():
            x0 = np.zeros((B.shape[0], d.shape[1]))
        else:
            x0 = parse_matrix_from_string(x0_str)

        tol = float(data.get('tolerance', 1e-5))
        max_iter = int(data.get('max_iter', 100))
        norm_choice = data.get('norm_choice', 'inf')
        
        result = simple_iteration(B, d, x0, tol=tol, max_iter=max_iter, norm_choice=norm_choice)
        formatted_result = format_simple_iteration_result(result)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500
    
@linear_algebra_bp.route('/inverse/jacobi', methods=['POST'])
def inverse_jacobi_route():
    try:
        data = request.json
        A = parse_matrix_from_string(data.get('matrix_a'))
        tol = float(data.get('tolerance', 1e-5))
        max_iter = int(data.get('max_iter', 100))
        x0_method = data.get('x0_method', 'method1')

        result = jacobi_inverse(A, tol=tol, max_iter=max_iter, x0_method=x0_method)
        formatted_result = format_inverse_jacobi_result(result)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500
    
@linear_algebra_bp.route('/inverse/newton', methods=['POST'])
def inverse_newton_route():
    try:
        data = request.json
        A = parse_matrix_from_string(data.get('matrix_a'))
        tol = float(data.get('tolerance', 1e-5))
        max_iter = int(data.get('max_iter', 100))
        x0_method = data.get('x0_method', 'method1') # Giữ nguyên 'method1' làm mặc định

        result = newton_inverse(A, tol=tol, max_iter=max_iter, x0_method=x0_method)
        formatted_result = format_inverse_newton_result(result)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500

@linear_algebra_bp.route('/inverse/gauss-seidel', methods=['POST'])
def inverse_gauss_seidel_route():
    try:
        data = request.json
        A = parse_matrix_from_string(data.get('matrix_a'))
        tol = float(data.get('tolerance', 1e-5))
        max_iter = int(data.get('max_iter', 100))
        x0_method = data.get('x0_method', 'method1')

        result = gauss_seidel_inverse(A, tol=tol, max_iter=max_iter, x0_method=x0_method)
        formatted_result = format_inverse_gauss_seidel_result(result)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500
    
@linear_algebra_bp.route('/svd', methods=['POST'])
def svd_route():
    """
    Route để thực hiện phân tích SVD.
    """
    try:
        data = request.json
        matrix_a_str = data.get('matrix_a')
        method = data.get('method', 'default')
        num_singular_str = data.get('num_singular')
        y_init_str = data.get('y_init')

        if not matrix_a_str:
            return jsonify({"error": "Vui lòng nhập ma trận A."}), 400

        A = parse_matrix_from_string(matrix_a_str)
        original_shape = A.shape

        result = {}
        if method == 'power':
            # Xử lý các tham số cho power method
            num_singular = int(num_singular_str) if num_singular_str else None
            y_init = parse_matrix_from_string(y_init_str) if y_init_str and y_init_str.strip() else None
            
            result = svd_power_deflation(A, num_singular=num_singular, y_init=y_init)
        else: # Mặc định là 'default'
            result = svd_numpy(A)
            
        formatted_result = format_svd_result(result, original_shape)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}"}), 500

@linear_algebra_bp.route('/eigen/danilevsky', methods=['POST'])
def danilevsky_route():
    try:
        data = request.json
        A = parse_matrix_from_string(data.get('matrix_a'))
        
        result = danilevsky_algorithm(A)
        
        formatted_result = format_danilevsky_result(result, A)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}\n{traceback.format_exc()}"}), 500

@linear_algebra_bp.route('/eigen/power-single', methods=['POST'])
def power_single_route():
    try:
        data = request.json
        A = parse_matrix_from_string(data.get('matrix_a'))
        tol = float(data.get('tolerance', 1e-9))
        max_iter = int(data.get('max_iter', 100))
        
        x0_str = data.get('x0')
        x0 = parse_matrix_from_string(x0_str) if x0_str and x0_str.strip() else None

        result = power_method_single(A, x0=x0, tol=tol, max_iter=max_iter)
        
        formatted_result = format_power_method_result(result, A)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        return jsonify({"error": f"Lỗi không mong muốn: {str(e)}\n{traceback.format_exc()}"}), 500

@linear_algebra_bp.route('/eigen/power-deflation', methods=['POST'])
def power_deflation_route():
    try:
        data = request.json
        A = parse_matrix_from_string(data.get('matrix_a'))
        num_values_str = data.get('num_values')
        num_values = int(num_values_str) if num_values_str and num_values_str.strip() else None
        
        tol = float(data.get('tolerance', 1e-6))
        max_iter = int(data.get('max_iter', 100))
        
        x0_str = data.get('x0')
        x0 = parse_matrix_from_string(x0_str) if x0_str and x0_str.strip() else None

        result = power_method_deflation(A, num_values=num_values, x0=x0, tol=tol, max_iter=max_iter)
        
        formatted_result = format_power_method_result(result, A)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        return jsonify({"error": f"Lỗi không mong muốn: {str(e)}\n{traceback.format_exc()}"}), 500

@linear_algebra_bp.route('/svd-approximation', methods=['POST'])
def svd_approximation_route():
    """
    Route để tính toán ma trận xấp xỉ bằng SVD.
    """
    try:
        data = request.json
        matrix_a_str = data.get('matrix_a')
        method = data.get('method', 'rank-k')
        value = data.get('value')

        if not matrix_a_str:
            return jsonify({"error": "Vui lòng nhập ma trận A."}), 400
        if value is None:
            return jsonify({"error": "Vui lòng cung cấp giá trị cho phương pháp xấp xỉ."}), 400

        A = parse_matrix_from_string(matrix_a_str)
        
        params = {}
        if method == 'rank-k':
            params['k'] = int(value)
        elif method == 'threshold':
            params['threshold'] = float(value)
        elif method == 'error-bound':
            params['error_bound'] = float(value)

        result = calculate_svd_approximation(A, method=method, **params)
        
        if not result.get("success"):
            return jsonify({"error": result.get("error", "Lỗi không xác định")}), 400

        formatted_result = format_svd_approximation_result(result)
        return jsonify(formatted_result), 200

    except (ValueError, np.linalg.LinAlgError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        return jsonify({"error": f"Đã xảy ra lỗi không mong muốn: {str(e)}\n{traceback.format_exc()}"}), 500
