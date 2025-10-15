# backend/routes/interpolation_routes.py
from flask import Blueprint, request, jsonify
from backend.numerical_methods.interpolation.chebyshev_nodes import chebyshev_nodes
from backend.api_formatters.interpolation import format_chebyshev_nodes_result
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