from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
import numpy as np
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.numerical_methods.interpolation.lagrange import lagrange_interpolation
from backend.numerical_methods.interpolation.divided_difference import divided_differences
from backend.numerical_methods.interpolation.finite_difference import finite_differences
if __name__ == "__main__":
    # Ví dụ sử dụng hàm lagrange_interpolation
    x_nodes = [2.1, 2.3, 2.5, 2.7, 2.9, 3.1]
    y_nodes = [0.5597, 1.0378, 1.5337, 1.9847, 2.3355, 2.5465]
    result = lagrange_interpolation(x_nodes, y_nodes)
    print("Hệ số đa thức nội suy Lagrange:", result['polynomial_coeffs'])

    # Ví dụ sử dụng hàm finite_differences
    divided_result = finite_differences(x_nodes, y_nodes)
    print("Bảng tỷ sai phân:", divided_result['finite_difference_table'])