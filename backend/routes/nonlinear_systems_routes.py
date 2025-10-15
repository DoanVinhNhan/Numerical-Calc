# backend/routes/nonlinear_systems_routes.py
from flask import Blueprint, request, jsonify
from backend.numerical_methods.nonlinear_systems.newton import solve_newton_system
from backend.numerical_methods.nonlinear_systems.newton_modified import solve_newton_modified_system
from backend.numerical_methods.nonlinear_systems.simple_iteration import solve_simple_iteration_system # Thêm import
from backend.api_formatters.nonlinear_systems import format_nonlinear_system_result
import traceback

nonlinear_systems_bp = Blueprint('nonlinear_systems', __name__, url_prefix='/api/nonlinear-systems')

@nonlinear_systems_bp.route('/solve', methods=['POST'])
def solve_system_route():
    try:
        data = request.json
        method = data.get('method')
        
        expr_list = data.get('expressions', [])
        x0_str_list = data.get('x0', [])
        
        if not expr_list or not x0_str_list:
            return jsonify({"error": "Vui lòng nhập đầy đủ hệ phương trình và vector ban đầu."}), 400
        
        n = len(expr_list)
        if n != len(x0_str_list):
                return jsonify({"error": "Số lượng phương trình và số lượng giá trị ban đầu phải bằng nhau."}), 400

        x0_list = [float(x) for x in x0_str_list]
        
        # Khai báo biến result
        result = None
        method_name = ""

        if method == 'newton':
            method_name = "Phương pháp Newton"
            result = solve_newton_system(
                n=n,
                expr_list=expr_list,
                x0_list=x0_list,
                stop_option=data.get('stop_option'),
                stop_value=data.get('stop_value'),
                norm_choice=data.get('norm_choice')
            )
        
        # Thêm logic cho Newton cải tiến
        elif method == 'newton_modified':
            method_name = "Phương pháp Newton Cải tiến"
            result = solve_newton_modified_system(
                n=n,
                expr_list=expr_list,
                x0_list=x0_list,
                stop_option=data.get('stop_option'),
                stop_value=data.get('stop_value'),
                norm_choice=data.get('norm_choice')
            )

        elif method == 'simple_iteration':
            method_name = "Phương pháp Lặp đơn"
            domain_str_list = data.get('domain', [])
            if n != len(domain_str_list):
                 return jsonify({"error": "Số lượng phương trình và số lượng miền xác định phải bằng nhau."}), 400
            
            a0_list = [float(d.split()[0]) for d in domain_str_list]
            b0_list = [float(d.split()[1]) for d in domain_str_list]

            result = solve_simple_iteration_system(
                n=n,
                expr_list=expr_list,
                x0_list=x0_list,
                a0_list=a0_list,
                b0_list=b0_list,
                stop_option=data.get('stop_option'),
                stop_value=data.get('stop_value')
            )

        else:
            return jsonify({"error": f"Phương pháp '{method}' không được hỗ trợ."}), 400
        
        formatted_result = format_nonlinear_system_result(method_name, result)
        return jsonify(formatted_result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Lỗi server: {str(e)}\n{traceback.format_exc()}"}), 500