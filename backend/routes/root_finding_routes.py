# backend/routes/root_finding_routes.py
from flask import Blueprint, request, jsonify
from backend.utils.expression_parser import parse_expression
from backend.numerical_methods.root_finding.bisection import bisection_method
from backend.api_formatters.root_finding import format_root_finding_result

root_finding_bp = Blueprint('root_finding', __name__, url_prefix='/api/root-finding')

@root_finding_bp.route('/solve', methods=['POST'])
def solve_root():
    try:
        data = request.json
        method = data.get('method')
        expr_str = data.get('expression')
        
        # Phân tích biểu thức f(x)
        parsed_func = parse_expression(expr_str)
        if not parsed_func["success"]:
            return jsonify({"error": parsed_func["error"]}), 400
        f = parsed_func["f"]

        # Lấy các tham số chung
        a = float(data.get('a'))
        b = float(data.get('b'))
        mode = data.get('stop_mode')
        value = data.get('stop_value')

        result = None
        if method == 'bisection':
            result = bisection_method(f, a, b, mode, value)
        # Thêm các phương pháp khác (newton, secant) ở đây
        # elif method == 'newton':
        #     ...
        else:
            return jsonify({"error": "Phương pháp không được hỗ trợ."}), 400
            
        formatted_result = format_root_finding_result(f"Chia đôi ({mode})", result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi không mong muốn: {str(e)}"}), 500