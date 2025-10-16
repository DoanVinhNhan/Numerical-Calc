from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
import numpy as np
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.numerical_methods.interpolation.lagrange import lagrange_interpolation
from backend.numerical_methods.interpolation.divided_difference import divided_differences
if __name__ == "__main__":
    # Ví dụ sử dụng hàm lagrange_interpolation
    x_nodes = [0, 1, 2]
    y_nodes = [1, 3, 2]
    result = lagrange_interpolation(x_nodes, y_nodes)
    print("Hệ số đa thức nội suy Lagrange:", result['polynomial_coeffs'])

    # Ví dụ sử dụng hàm divided_differences
    divided_result = divided_differences(x_nodes, y_nodes)
    print("Bảng tỷ sai phân:", divided_result['divided_difference_table'])