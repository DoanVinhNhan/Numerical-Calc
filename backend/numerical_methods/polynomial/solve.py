# backend/numerical_methods/polynomial/solve.py
import numpy as np

def _format_poly_str(coeffs):
    """Tạo một chuỗi đa thức ở định dạng LaTeX từ danh sách các hệ số."""
    terms = []
    degree = len(coeffs) - 1
    for i, c in enumerate(coeffs):
        if np.isclose(c, 0):
            continue
        
        power = degree - i
        
        sign = " - " if c < 0 else " + "
        c_abs = abs(c)
        
        if np.isclose(c_abs, 1) and power != 0:
            coeff_str = ""
        else:
            coeff_str = f"{c_abs:g}"

        if power > 1:
            var_str = f"x^{{{power}}}"
        elif power == 1:
            var_str = "x"
        else: # power == 0
            var_str = ""
        
        term = f"{coeff_str}{var_str}"

        if i == 0:
            terms.append(f"-{term}" if sign.strip() == "-" else term)
        else:
            terms.append(f"{sign}{term}")
            
    poly_str = " ".join(terms).lstrip(' +')
    return poly_str if poly_str else "0"

def _find_root_bounds(coeffs):
    """Tìm khoảng chứa nghiệm thực dựa trên phương pháp của Lagrange."""
    if not any(coeffs) or coeffs[0] == 0:
        return None, None

    a = np.array(coeffs, dtype=float)
    a[0] = np.abs(a[0])
    
    first_neg_idx = next((i for i, c in enumerate(a) if c < 0), -1)
    
    N1 = 0
    if first_neg_idx != -1:
        max_abs_neg = np.max(np.abs(a[first_neg_idx:]))
        N1 = 1 + (max_abs_neg / a[0])**(1/first_neg_idx)
    
    b = a.copy()
    for i in range(1, len(b)):
        if i % 2 != 0:
            b[i] = -b[i]
            
    first_neg_idx_b = next((i for i, c in enumerate(b) if c < 0), -1)
        
    N2 = 0
    if first_neg_idx_b != -1:
        max_abs_neg_b = np.max(np.abs(b[first_neg_idx_b:]))
        N2 = 1 + (max_abs_neg_b / b[0])**(1/first_neg_idx_b)

    return -N2, N1

def _bisection(p, a, b, tol, max_iter):
    """Hàm chia đôi nội bộ để tìm nghiệm trong khoảng [a, b]."""
    fa = p(a)
    steps = []
    
    if fa * p(b) >= 0:
        return None, []

    for i in range(max_iter):
        c = (a + b) / 2.0
        fc = p(c)
        steps.append({'k': i + 1, 'a': a, 'b': b, 'c': c, 'fc': fc})
        
        if abs(b - a) / 2.0 < tol or fc == 0:
            return c, steps
        
        if fa * fc < 0:
            b = c
        else:
            a = c
            fa = fc
            
    return (a + b) / 2.0, steps

def solve_polynomial_roots(coeffs, tol=1e-7, max_iter=100):
    """Giải phương trình đa thức và trả về các bước trung gian."""
    if len(coeffs) < 2:
        raise ValueError("Đa thức phải có bậc ít nhất là 1.")

    p = np.poly1d(coeffs)
    p_deriv = p.deriv()

    lower_bound, upper_bound = _find_root_bounds(coeffs)
    if lower_bound is None:
        raise ValueError("Hệ số đầu tiên không được bằng 0.")

    critical_points = p_deriv.r
    real_critical_points = sorted([cp.real for cp in critical_points if np.isclose(cp.imag, 0)])

    search_points = sorted(list(set([lower_bound] + real_critical_points + [upper_bound])))
    
    intervals = []
    for i in range(len(search_points) - 1):
        intervals.append((search_points[i], search_points[i+1]))

    found_roots = []
    for a, b in intervals:
        a_check, b_check = a - tol, b + tol
        
        if p(a_check) * p(b_check) < 0:
            root, bisection_steps = _bisection(p, a_check, b_check, tol, max_iter)
            if root is not None and not any(np.isclose(root, r['root_value']) for r in found_roots):
                found_roots.append({
                    "root_value": root,
                    "interval": [a, b],
                    "bisection_steps": bisection_steps
                })
    
    return {
        "polynomial_str": _format_poly_str(coeffs),
        "bounds": [lower_bound, upper_bound],
        "critical_points": real_critical_points,
        "search_intervals": intervals,
        "found_roots": found_roots
    }