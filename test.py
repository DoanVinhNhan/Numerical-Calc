from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
import numpy as np
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.numerical_methods.interpolation.lagrange import lagrange_interpolation
from backend.numerical_methods.interpolation.divided_difference import divided_differences
from backend.numerical_methods.interpolation.finite_difference import finite_differences
from backend.numerical_methods.interpolation.newton import newton_interpolation_equidistant, newton_interpolation_divided_difference
from backend.numerical_methods.horner_table.change_variables import change_variables
from backend.numerical_methods.interpolation.central import central_gauss_i
if __name__ == "__main__":
    x_nodes = [1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6]
    y_nodes = [0.524, -0.084, -0.964, -2.121, -3.558, -5.272, -7.255, -9.494, -11.973]

    result = central_gauss_i(x_nodes, y_nodes)
    print("Bảng sai phân hữu hạn:")
    for row in result['finite_difference_table']:
        print(row)
    print("Sai phân trung tâm:")
    print(result['central_finite_diffs'])
    print("Bảng tích w_i(t):")
    for coeffs in result['w_table']:
        print(coeffs)
    print("a_coeffs:")
    print(result['a_coeffs'])
    print("Đa thức nội suy (hệ số):")
    print(result['polynomial_coeffs'])