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

    gauss = central_gauss_i(x_nodes, y_nodes)
    coefficients = gauss['polynomial_coeffs_t']
    print("Hệ số đa thức nội suy trung tâm Gauss I:", coefficients)
    result = synthetic_division(coefficients, (1.43-1.8)/0.2)['value']
    print("Kết quả:", result)

    lagrange = lagrange_interpolation(x_nodes, y_nodes)
    coefficients = lagrange['polynomial_coeffs']
    print("Hệ số đa thức nội suy Lagrange:", coefficients)
    result = synthetic_division(coefficients, 1.43)['value']
    print("Kết quả:", result)