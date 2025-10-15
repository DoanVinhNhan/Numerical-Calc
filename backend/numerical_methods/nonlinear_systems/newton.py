# backend/numerical_methods/nonlinear_systems/newton.py
import numpy as np
from sympy import symbols, sympify, Matrix, latex

def solve_newton_system(n, expr_list, x0_list, stop_option, stop_value, norm_choice, max_iter=200):
    """
    Giải hệ phương trình phi tuyến F(X) = 0 bằng phương pháp Newton.
    """
    try:
        # 1. Khởi tạo các biến symbolic và ma trận
        variables = symbols(f'x1:{n+1}')
        F = Matrix([sympify(expr) for expr in expr_list])
        X = Matrix(x0_list)
        J = F.jacobian(variables)
        iterations_data = []

        # 2. Vòng lặp chính
        # TH1: Dừng theo số lần lặp
        if stop_option == 'iterations':
            max_iter = int(stop_value)
            for k in range(max_iter):
                F_val = F.subs({variables[i]: X[i] for i in range(n)}).evalf()
                J_val = J.subs({variables[i]: X[i] for i in range(n)}).evalf()

                if abs(J_val.det().evalf()) < 1e-12:
                    raise ValueError(f"Ma trận Jacobi suy biến tại bước lặp {k+1}.")
                
                # Công thức lặp Newton: X_k+1 = X_k - J(X_k)^-1 * F(X_k)
                delta_X = J_val.inv() * F_val
                X = X - delta_X
                
                step_info = {f"x{i+1}": float(X[i]) for i in range(n)}
                step_info['k'] = k + 1
                iterations_data.append(step_info)
        
        # TH2: Dừng theo sai số
        else:
            tol = float(stop_value)
            for k in range(max_iter):
                X_prev = X.copy()
                F_val = F.subs({variables[i]: X[i] for i in range(n)}).evalf()
                J_val = J.subs({variables[i]: X[i] for i in range(n)}).evalf()

                if abs(J_val.det().evalf()) < 1e-12:
                    raise ValueError(f"Ma trận Jacobi suy biến tại bước lặp {k+1}.")

                delta_X = J_val.inv() * F_val
                X = X - delta_X

                # Tính toán sai số
                diff_vec = np.array(X.tolist(), dtype=float) - np.array(X_prev.tolist(), dtype=float)
                
                if norm_choice == '1':
                    error = float(np.linalg.norm(diff_vec, 1))
                    norm_X = float(np.linalg.norm(np.array(X.tolist(), dtype=float), 1))
                else: # Mặc định là chuẩn vô cùng
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
            else: # Nếu vòng lặp kết thúc mà không break
                raise ValueError(f"Phương pháp không hội tụ sau {max_iter} lần lặp.")
        
        # 3. Chuẩn bị kết quả trả về
        # Chuyển ma trận Jacobi symbolic sang LaTeX
        try:
            J_latex = [[latex(elem) for elem in row] for row in J.tolist()]
        except Exception:
            J_latex = [[str(elem) for elem in row] for row in J.tolist()]
            
        return {
            "status": "success",
            "solution": [float(val) for val in X],
            "iterations": len(iterations_data),
            "jacobian_matrix_latex": J_latex,
            "steps": iterations_data,
            "message": f"Hội tụ sau {len(iterations_data)} lần lặp."
        }

    except (ValueError, TypeError) as e:
        raise e # Ném lại lỗi để route xử lý
    except Exception as e:
        import traceback
        raise Exception(f"Lỗi không xác định trong thuật toán: {str(e)}\n{traceback.format_exc()}")