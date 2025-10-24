from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
import numpy as np
import math
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.numerical_methods.interpolation.lagrange import lagrange_interpolation
from backend.numerical_methods.interpolation.divided_difference import divided_differences
from backend.numerical_methods.interpolation.finite_difference import finite_differences
from backend.numerical_methods.interpolation.newton import newton_interpolation_equidistant, newton_interpolation_divided_difference
from backend.numerical_methods.horner_table.change_variables import change_variables
from backend.numerical_methods.interpolation.central import central_gauss_i, central_gauss_ii
if __name__ == "__main__":
    """
    x_nodes = [1.6, 1.8, 2.0, 2.2, 2.4]
    y_nodes = [4.23, 3.67, 2.99, 1.24, 0.87]

    finite_differences_table = finite_differences(x_nodes, y_nodes)["finite_difference_table"]
    f_coeff = [finite_differences_table[i][i+1] for i in range(len(finite_differences_table))]

    t_0 = (4 - 4.23)/f_coeff[1]
    print(t_0)
    t = t_0
    t_prev = t_0+100
    count = 0
    while (abs(t-t_prev) >1e-5):
        count+=1
        t_prev = t
        sum_values = 0
        for i in range(2,len(x_nodes)):
            prod = 1
            for j in range(i):
                prod = prod*(t_prev-j)
            sum_values = sum_values + f_coeff[i]*prod/ math.factorial(i)

        t = t_0 - (sum_values)/f_coeff[1]
        print(t)
    x= 0.2*t+1.6
    print(x)
    print(count)

    coeffs = newton_interpolation_equidistant(x_nodes, y_nodes)['forward_interpolation']['polynomial_coeffs_x']
    result = synthetic_division(coeffs, x)['value']
    print(result)
    print(t_0)
    """

    x_nodes = [9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10]
    y_nodes = [9.4341319, 9.4307764, 9.4261142, 9.421191, 9.4170553, 9.4147476, 9.41529, 9.4196762, 9.4288617]
    result = central_gauss_i(x_nodes, y_nodes)['polynomial_coeffs_t']
    print(result)
    value = synthetic_division(result, 9.68)['value']
    print(value)
