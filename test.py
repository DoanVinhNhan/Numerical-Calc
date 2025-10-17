from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
import numpy as np
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.numerical_methods.interpolation.lagrange import lagrange_interpolation
from backend.numerical_methods.interpolation.divided_difference import divided_differences
from backend.numerical_methods.interpolation.finite_difference import finite_differences
from backend.numerical_methods.interpolation.newton import newton_interpolation_equidistant
if __name__ == "__main__":
    # Ví dụ sử dụng hàm lagrange_interpolation
    x_nodes = [2.1, 2.3, 2.5, 2.7, 2.9, 3.1]
    y_nodes = [0.5597, 1.0378, 1.5337, 1.9847, 2.3355, 2.5465]
    result_lagrange = lagrange_interpolation(x_nodes, y_nodes)
    print("Hệ số đa thức nội suy Lagrange:", result_lagrange['polynomial_coeffs'])
    # Ví dụ sử dụng hàm newton_interpolation_equidistant
    result_newton = newton_interpolation_equidistant(x_nodes, y_nodes)
    print("Hệ số đa thức nội suy Newton Tiến theo t:", result_newton['polynomial_coeffs_forward_t'])
    print("Hệ số đa thức nội suy Newton Tiến theo x:", result_newton['polynomial_coeffs_forward_x'])
    print("Hệ số đa thức nội suy Newton Lùi theo t:", result_newton['polynomial_coeffs_backward_t'])
    print("Hệ số đa thức nội suy Newton Lùi theo x:", result_newton['polynomial_coeffs_backward_x'])
