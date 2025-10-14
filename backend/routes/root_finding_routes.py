# backend/routes/root_finding_routes.py
from flask import Blueprint, request, jsonify
from backend.utils.expression_parser import parse_expression
from backend.numerical_methods.root_finding.bisection import bisection_method
from backend.numerical_methods.root_finding.secant import secant_method
from backend.numerical_methods.root_finding.newton import newton_method
from backend.numerical_methods.root_finding.simple_iteration import simple_iteration_method # <<< THÊM
from backend.api_formatters.root_finding import format_root_finding_result

root_finding_bp = Blueprint('root_finding', __name__, url_prefix='/api/root-finding')

@root_finding_bp.route('/solve', methods=['POST'])
def solve_root():
    try:
        data = request.json
        method = data.get('method')
        
        # ... (code xử lý a, b, mode, value không đổi)
        a = float(data.get('a'))
        b = float(data.get('b'))
        mode = data.get('stop_mode')
        value = data.get('stop_value')
        
        result = None
        method_name = ""

        if method == 'simple_iteration': # <<< THÊM KHỐI LOGIC NÀY
            method_name = "Lặp đơn"
            phi_expr_str = data.get('phi_expression')
            x0 = float(data.get('x0'))
            
            parsed_phi = parse_expression(phi_expr_str)
            if not parsed_phi["success"]:
                return jsonify({"error": parsed_phi["error"]}), 400

            result = simple_iteration_method(
                phi=parsed_phi["f"], 
                phi_prime=parsed_phi["f_prime"],
                a=a, b=b, x0=x0, mode=mode, value=value
            )
        else:
            expr_str = data.get('expression')
            parsed_func = parse_expression(expr_str)
            if not parsed_func["success"]:
                return jsonify({"error": parsed_func["error"]}), 400
            
            f, f_prime, f_double_prime = parsed_func["f"], parsed_func["f_prime"], parsed_func["f_double_prime"]

            if method == 'bisection':
                method_name = "Chia đôi"
                result = bisection_method(f, a, b, mode, value)
            elif method == 'secant':
                method_name = "Dây cung (Secant)"
                stop_condition = data.get('adv_stop_condition', 'f_xn')
                result = secant_method(f, f_prime, f_double_prime, a, b, mode, value, stop_condition)
            elif method == 'newton':
                method_name = "Newton (Tiếp tuyến)"
                stop_condition = data.get('adv_stop_condition', 'f_xn')
                x0 = float(data.get('x0'))
                result = newton_method(f, f_prime, f_double_prime, a, b, x0, mode, value, stop_condition)
            else:
                return jsonify({"error": "Phương pháp không được hỗ trợ."}), 400
            
        formatted_result = format_root_finding_result(f"{method_name}", result, mode, data.get('adv_stop_condition'))
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        return jsonify({"error": f"Lỗi không mong muốn: {str(e)}\n{traceback.format_exc()}"}), 500