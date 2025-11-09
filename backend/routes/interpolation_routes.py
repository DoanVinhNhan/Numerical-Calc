# backend/routes/interpolation_routes.py
from flask import Blueprint, request, jsonify
from backend.numerical_methods.interpolation.chebyshev_nodes import chebyshev_nodes
from backend.api_formatters.interpolation import format_chebyshev_nodes_result, format_finite_difference_result
from backend.numerical_methods.interpolation.lagrange import lagrange_interpolation
from backend.api_formatters.interpolation import format_lagrange_interpolation_result
from backend.numerical_methods.interpolation.divided_difference import divided_differences
from backend.numerical_methods.interpolation.finite_difference import finite_differences
from backend.api_formatters.interpolation import format_divided_difference_result
from backend.numerical_methods.interpolation.newton import newton_interpolation_equidistant
from backend.api_formatters.interpolation import format_newton_interpolation_result
from backend.numerical_methods.interpolation.newton import newton_interpolation_equidistant, newton_interpolation_divided_difference 
from backend.api_formatters.interpolation import format_newton_interpolation_result, format_newton_divided_interpolation_result
from backend.numerical_methods.interpolation.central import central_gauss_i, central_gauss_ii, stirlin_interpolation, bessel_interpolation
from backend.api_formatters.interpolation import format_central_gauss_i_result, format_central_gauss_ii_result, format_stirling_interpolation_result, format_bessel_interpolation_result
from backend.numerical_methods.interpolation.spline import spline_linear, spline_quadratic, spline_cubic
from backend.numerical_methods.interpolation.least_squares import least_squares_approximation
from backend.api_formatters.interpolation import format_spline_result, format_lsq_result
from backend.numerical_methods.interpolation.node_selection import select_interpolation_nodes
from backend.api_formatters.interpolation import format_node_selection_result
from backend.numerical_methods.interpolation.find_intervals import find_root_intervals
from backend.api_formatters.interpolation import format_find_intervals_result
from backend.numerical_methods.interpolation.inverse_interpolation import solve_inverse_iterative
from backend.api_formatters.interpolation import format_inverse_interpolation_result
import io
import traceback

interpolation_bp = Blueprint('interpolation', __name__, url_prefix='/api/interpolation')

@interpolation_bp.route('/chebyshev-nodes', methods=['POST'])
def chebyshev_nodes_route():
    try:
        data = request.json
        a = float(data.get('a'))
        b = float(data.get('b'))
        n = int(data.get('n'))

        # Gọi hàm tính toán
        result = chebyshev_nodes(a, b, n)

        # Định dạng và trả về kết quả
        formatted_result = format_chebyshev_nodes_result(result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500
    
@interpolation_bp.route('/lagrange', methods=['POST'])
def lagrange_route():
    try:
        data = request.json
        x_nodes_str = data.get('x_nodes', '').split()
        y_nodes_str = data.get('y_nodes', '').split()

        if not x_nodes_str or not y_nodes_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ các mốc x và giá trị y."}), 400

        x_nodes = [float(x) for x in x_nodes_str]
        y_nodes = [float(y) for y in y_nodes_str]
        
        result = lagrange_interpolation(x_nodes, y_nodes)
        
        formatted_result = format_lagrange_interpolation_result(result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500


@interpolation_bp.route('/divided-difference', methods=['POST'])
def divided_difference_route():
    try:
        data = request.json
        x_nodes_str = data.get('x_nodes', '').split()
        y_nodes_str = data.get('y_nodes', '').split()

        if not x_nodes_str or not y_nodes_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ các mốc x và giá trị y."}), 400

        x_nodes = [float(x) for x in x_nodes_str]
        y_nodes = [float(y) for y in y_nodes_str]

        result = divided_differences(x_nodes, y_nodes)

        formatted_result = format_divided_difference_result(result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500
    
@interpolation_bp.route('/finite-difference', methods=['POST'])
def finite_difference_route():
    try:
        data = request.json
        x_nodes_str = data.get('x_nodes', '').split()
        y_nodes_str = data.get('y_nodes', '').split()

        if not x_nodes_str or not y_nodes_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ các mốc x và giá trị y."}), 400

        x_nodes = [float(x) for x in x_nodes_str]
        y_nodes = [float(y) for y in y_nodes_str]

        result = finite_differences(x_nodes, y_nodes)

        formatted_result = format_finite_difference_result(result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500
    
@interpolation_bp.route('/newton-interpolation', methods=['POST'])
def newton_interpolation_route():
    try:
        data = request.json
        x_nodes_str = data.get('x_nodes', '').split()
        y_nodes_str = data.get('y_nodes', '').split()
        method_type = data.get('method_type', 'equidistant')

        if not x_nodes_str or not y_nodes_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ các mốc x và giá trị y."}), 400

        x_nodes = [float(x) for x in x_nodes_str]
        y_nodes = [float(y) for y in y_nodes_str]

        if method_type == 'arbitrary': # <<< THÊM: Xử lý mốc bất kỳ
            result = newton_interpolation_divided_difference(x_nodes, y_nodes)
            formatted_result = format_newton_divided_interpolation_result(result) # <<< SỬ DỤNG FORMATTER MỚI
        else: # Mặc định là mốc cách đều
            result = newton_interpolation_equidistant(x_nodes, y_nodes)
            formatted_result = format_newton_interpolation_result(result)

        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500
    
@interpolation_bp.route('/central-interpolation', methods=['POST'])
def central_interpolation_route():
    try:
        data = request.json
        x_nodes_str = data.get('x_nodes', '').split()
        y_nodes_str = data.get('y_nodes', '').split()
        method_type = data.get('method_type', 'gauss_i') # Lấy loại PP trung tâm

        if not x_nodes_str or not y_nodes_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ các mốc x và giá trị y."}), 400

        x_nodes = [float(x) for x in x_nodes_str]
        y_nodes = [float(y) for y in y_nodes_str]

        result = None
        formatted_result = None

        if method_type == 'gauss_i':
            result = central_gauss_i(x_nodes, y_nodes)
            formatted_result = format_central_gauss_i_result(result)
        elif method_type == 'gauss_ii':
            # <<< THÊM MỚI: Xử lý Gauss II >>>
            result = central_gauss_ii(x_nodes, y_nodes)
            formatted_result = format_central_gauss_ii_result(result)
        elif method_type == 'stirlin':
            # <<< THÊM MỚI: Xử lý Stirling >>>
            result = stirlin_interpolation(x_nodes, y_nodes)
            formatted_result = format_stirling_interpolation_result(result)
        elif method_type == 'bessel':
            # <<< THÊM MỚI: Xử lý Bessel >>>
            result = bessel_interpolation(x_nodes, y_nodes)
            formatted_result = format_bessel_interpolation_result(result)
        else:
            return jsonify({"error": f"Phương pháp nội suy trung tâm '{method_type}' không hợp lệ."}), 400

        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500
    
@interpolation_bp.route('/spline', methods=['POST'])
def spline_route():
    try:
        data = request.json
        x_nodes_str = data.get('x_nodes', '').split()
        y_nodes_str = data.get('y_nodes', '').split()
        spline_type = data.get('spline_type', 'linear')

        if not x_nodes_str or not y_nodes_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ các mốc x và giá trị y."}), 400

        x_nodes = [float(x) for x in x_nodes_str]
        y_nodes = [float(y) for y in y_nodes_str]

        result = None
        if spline_type == 'linear':
            result = spline_linear(x_nodes, y_nodes)
        elif spline_type == 'quadratic':
            boundary_m1 = float(data.get('boundary_m1', 0.0))
            result = spline_quadratic(x_nodes, y_nodes, boundary_m1)
        elif spline_type == 'cubic':
            boundary_start = float(data.get('boundary_start', 0.0))
            boundary_end = float(data.get('boundary_end', 0.0))
            result = spline_cubic(x_nodes, y_nodes, boundary_start, boundary_end)
        else:
            return jsonify({"error": "Loại spline không được hỗ trợ."}), 400

        formatted_result = format_spline_result(result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500

@interpolation_bp.route('/least-squares', methods=['POST'])
def least_squares_route():
    try:
        data = request.json
        x_nodes_str = data.get('x_nodes', '').split()
        y_nodes_str = data.get('y_nodes', '').split()
        # Nhận mảng các chuỗi hàm cơ sở, đã được split từ frontend
        basis_funcs_str = data.get('basis_funcs', [])

        if not x_nodes_str or not y_nodes_str or not basis_funcs_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ mốc x, giá trị y, và các hàm cơ sở."}), 400

        x_nodes = [float(x) for x in x_nodes_str]
        y_nodes = [float(y) for y in y_nodes_str]

        result = least_squares_approximation(x_nodes, y_nodes, basis_funcs_str)

        # Hàm format LSQ đơn giản là trả về kết quả vì nó đã được định dạng
        formatted_result = format_lsq_result(result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500
    
@interpolation_bp.route('/select-nodes', methods=['POST'])
def select_nodes_route():
    try:
        # Kiểm tra xem file có trong request không
        if 'file' not in request.files:
            return jsonify({"error": "Không tìm thấy file nào trong request."}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Không có file nào được chọn."}), 400

        # Đọc dữ liệu từ file
        try:
            # Đọc file dưới dạng bytes và đưa vào BytesIO
            file_stream = io.BytesIO(file.read())
        except Exception as e:
            return jsonify({"error": f"Không thể đọc file: {str(e)}"}), 400

        # Lấy các tham số khác từ form
        data = request.form
        x_bar = float(data.get('x_bar'))
        num_nodes = int(data.get('num_nodes'))
        method = data.get('method', 'both')

        # Gọi hàm xử lý
        result = select_interpolation_nodes(file_stream, x_bar, num_nodes, method)
        
        # Định dạng và trả về
        formatted_result = format_node_selection_result(result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500
    
@interpolation_bp.route('/find-intervals', methods=['POST'])
def find_intervals_route():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Không tìm thấy file nào trong request."}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Không có file nào được chọn."}), 400

        file_stream = io.BytesIO(file.read())
        
        data = request.form
        y_bar = float(data.get('y_bar'))
        num_nodes = int(data.get('num_nodes'))
        method = data.get('method', 'both')

        # Gọi hàm xử lý với các tham số mới (bao gồm phương thức mở rộng)
        result = find_root_intervals(file_stream, y_bar, num_nodes, method)
        
        formatted_result = format_find_intervals_result(result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500
    
@interpolation_bp.route('/inverse-iterative', methods=['POST'])
def inverse_iterative_route():
    try:
        data = request.json
        x_nodes_str = data.get('x_nodes', '').split()
        y_nodes_str = data.get('y_nodes', '').split()
        
        if not x_nodes_str or not y_nodes_str:
            return jsonify({"error": "Vui lòng nhập đầy đủ các mốc x và giá trị y."}), 400

        y_bar = float(data.get('y_bar'))
        epsilon = float(data.get('epsilon'))
        method = data.get('method') # 'forward' or 'backward'

        x_nodes = [float(x) for x in x_nodes_str]
        y_nodes = [float(y) for y in y_nodes_str]
        
        result = solve_inverse_iterative(x_nodes, y_nodes, y_bar, epsilon, method)
        
        formatted_result = format_inverse_interpolation_result(result)
        return jsonify(formatted_result)
        
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500