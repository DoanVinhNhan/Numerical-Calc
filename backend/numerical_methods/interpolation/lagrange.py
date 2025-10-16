#backend/numerical_methods/interpolation/lagrange.py
import numpy as np
from backend.numerical_methods.horner_table.all_derivatives import all_derivatives
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
from backend.numerical_methods.horner_table.w_function import calculate_w_function

def lagrange_interpolation(x_nodes, y_nodes):
    """
    Đa thức nội suy Lagrange dựa trên các điểm (x_i, y_i).
    Trong đó, đa thức Lagrange được định nghĩa là:
        P(x) = \sum\limits_{i=0}^{n}\frac{y_i}{\prod\limits_{k\ne i}x_i-x_k}\frac{w_{n+1}(x)}{x-x_i}.
    Parameters:
        x_nodes (list of float): Các điểm x_i.
        x_nodes (list of float): Các điểm y_i tương ứng.
    Returns:
        dict: Chứa các bước tính toán và đa thức kết quả.
    """
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)

    if len(x_nodes) != len(y_nodes):
        raise ValueError("Số lượng mốc x và giá trị y phải bằng nhau.")
    n = len(x_nodes)
    if n == 0:
        return {
            "polynomial_coeffs": [],
            "steps": [],
            "w_coeffs": [1.0]
        }
    for i in range (n):
        if np.sum(np.isclose(x_nodes[i], x_nodes)) > 1:
            raise ValueError(f"Các mốc x phải phân biệt nhau. Mốc x={x_nodes[i]} bị lặp lại.")

    # w_{n+1}(x) = (x - x_0)(x - x_1)...(x - x_n)
    w_result = calculate_w_function(x_nodes)
    w_coeffs = w_result['final_coeffs']
    w_steps = w_result['steps']

    # w_{n+1}(x)/ (x - x_i)
    division_tables = []
    quotients = []
    for i in range(n):
        division_result = synthetic_division(w_coeffs, x_nodes[i])
        division_tables.append(division_result['division_table'])
        quotients.append(division_result['quotient_coeffs'])

    # D_i = (x_i-x_0)(x_i-x_1)...(x_i-x_{i-1})(x_i-x_{i+1})...(x_i-x_n)
    #     = w'_{n+1}(x_i)
    D = []
    D_steps = []
    for i in range(n):
        derivative_result = all_derivatives(w_coeffs, x_nodes[i], order=1)
        D.append(derivative_result['derivatives'][1]) # Lấy giá trị đạo hàm bậc 1
        D_steps.append(derivative_result['steps'])

    # y_i/D_i*w_{n+1}(x)/(x-x_i)
    terms = []
    for i in range(n):
        term_coeffs = quotients[i] * (y_nodes[i] / D[i])
        terms.append(term_coeffs)

    # Tính toán đa thức nội suy Lagrange
    lagrange_polynomial = np.sum(terms, axis=0)
    return {
        "polynomial_coeffs": lagrange_polynomial.tolist(),
        "w_calculation": {
            "coeffs": w_coeffs, # Đây đã là list từ calculate_w_function
            "steps": w_steps  # w_steps đã chứa list
        },
        "calculation_steps": [
            {
                "i": i,
                "xi": float(x_nodes[i]),
                "yi": float(y_nodes[i]),
                "w_division_table": division_tables[i].tolist(),
                "w_over_x_minus_xi_coeffs": quotients[i].tolist(),
                "Di_value": float(D[i]),
                "Di_calculation_steps": D_steps[i], # all_derivatives đã trả về list
                "term_coeffs": terms[i].tolist()
            } for i in range(n)
        ]
    }
