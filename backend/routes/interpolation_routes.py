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