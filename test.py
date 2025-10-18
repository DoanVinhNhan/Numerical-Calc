from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
import numpy as np
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.numerical_methods.interpolation.lagrange import lagrange_interpolation
from backend.numerical_methods.interpolation.divided_difference import divided_differences
from backend.numerical_methods.interpolation.finite_difference import finite_differences
from backend.numerical_methods.interpolation.newton import newton_interpolation_equidistant, newton_interpolation_divided_difference
from backend.numerical_methods.horner_table.change_variables import change_variables
if __name__ == "__main__":
    x_nodes = [2.1, 2.3, 2.5, 2.7, 2.9, 3.1]
    y_nodes = [0.5597, 1.0378, 1.5337, 1.9847, 2.3355, 2.5465]

    result_1 = newton_interpolation_equidistant(x_nodes, y_nodes)['forward_interpolation']['polynomial_coeffs_x']
    result_2 = lagrange_interpolation(x_nodes, y_nodes)['polynomial_coeffs']
    result_3 = newton_interpolation_divided_difference(x_nodes, y_nodes)['forward_interpolation']['polynomial_coeffs']
    print("Kết quả nội suy Newton mốc cách đều:")
    print(result_1)
    print("Kết quả nội suy Lagrange:")
    print(result_2)
    print("Kết quả nội suy Newton mốc bất kỳ:")
    print(result_3)