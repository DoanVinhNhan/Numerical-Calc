# backend/numerical_methods/nonlinear_systems/newton_modified.py
import numpy as np
from sympy import symbols, sympify, Matrix

def solve_newton_modified_system(n, expr_list, x0_list, stop_option, stop_value, norm_choice, max_iter=200):
    """
    Giải hệ phương trình phi tuyến F(X) = 0 bằng phương pháp Newton cải tiến.
    Ma trận Jacobi chỉ được tính và nghịch đảo một lần tại X_0.
    """
    try:
        # 1. Khởi tạo
        variables = symbols(f'x1:{n+1}')
        F = Matrix([sympify(expr) for expr in expr_list])
        X = Matrix(x0_list)
        J = F.jacobian(variables)
        
        # 2. Tính J(X_0)^-1 một lần duy nhất
        J0_val = J.subs({variables[i]: X[i] for i in range(n)}).evalf()
        if abs(J0_val.det().evalf()) < 1e-12:
            raise ValueError("Ma trận Jacobi tại điểm ban đầu J(X₀) suy biến, không thể nghịch đảo.")
        
        J0_inv = J0_val.inv()
        iterations_data = []

        # 3. Vòng lặp chính
        if stop_option == 'iterations':
            max_iter = int(stop_value)
            for k in range(max_iter):
                F_val = F.subs({variables[i]: X[i] for i in range(n)}).evalf()
                X = X - J0_inv * F_val # Sử dụng J0_inv đã tính
                
                step_info = {f"x{i+1}": float(X[i]) for i in range(n)}
                step_info['k'] = k + 1
                iterations_data.append(step_info)
        else:
            tol = float(stop_value)
            for k in range(max_iter):
                X_prev = X.copy()
                F_val = F.subs({variables[i]: X[i] for i in range(n)}).evalf()
                X = X - J0_inv * F_val # Sử dụng J0_inv đã tính

                # Tính toán sai số
                diff_vec = np.array(X.tolist(), dtype=float) - np.array(X_prev.tolist(), dtype=float)
                
                if norm_choice == '1':
                    error = float(np.linalg.norm(diff_vec, 1))
                    norm_X = float(np.linalg.norm(np.array(X.tolist(), dtype=float), 1))
                else: # Chuẩn vô cùng
                    error = float(np.linalg.norm(diff_vec, np.inf))
                    norm_X = float(np.linalg.norm(np.array(X.tolist(), dtype=float), np.inf))
                
                rel_err = error / norm_X if norm_X > 1e-12 else float('inf')

                step_info = {f"x{i+1}": float(X[i]) for i in range(n)}
                step_info['k'] = k + 1
                step_info['error'] = error
                step_info['relative_error'] = rel_err
                iterations_data.append(step_info)

                if (stop_option == 'absolute_error' and error < tol) or \
                   (stop_option == 'relative_error' and rel_err < tol):
                    break
            else:
                raise ValueError(f"Phương pháp không hội tụ sau {max_iter} lần lặp.")

        # 4. Trả về kết quả
        return {
            "status": "success",
            "solution": [float(val) for val in X],
            "iterations": len(iterations_data),
            "J0_inv_matrix": [[float(v) for v in row] for row in J0_inv.tolist()],
            "steps": iterations_data,
            "message": f"Hội tụ sau {len(iterations_data)} lần lặp."
        }
    except (ValueError, TypeError) as e:
        raise e
    except Exception as e:
        import traceback
        raise Exception(f"Lỗi không xác định: {str(e)}\n{traceback.format_exc()}")