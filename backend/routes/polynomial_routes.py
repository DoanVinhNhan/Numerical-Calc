# backend/routes/polynomial_routes.py
from flask import Blueprint, request, jsonify
from backend.numerical_methods.polynomial.solve import solve_polynomial_roots

polynomial_bp = Blueprint('polynomial', __name__, url_prefix='/api/polynomial')

@polynomial_bp.route('/solve', methods=['POST'])
def solve_polynomial_route():
    try:
        data = request.json
        coeffs_str = data.get('coeffs', '').split()
        coeffs = [float(c) for c in coeffs_str]
        
        tol = float(data.get('tolerance', 1e-7))
        max_iter = int(data.get('max_iter', 100))

        result = solve_polynomial_roots(coeffs, tol, max_iter)
        
        return jsonify(result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        return jsonify({"error": f"Lỗi không xác định: {traceback.format_exc()}"}), 500