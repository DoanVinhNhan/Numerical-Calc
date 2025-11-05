from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
import numpy as np
import math
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.numerical_methods.interpolation.lagrange import lagrange_interpolation
from backend.numerical_methods.interpolation.divided_difference import divided_differences
from backend.numerical_methods.interpolation.finite_difference import finite_differences
from backend.numerical_methods.interpolation.newton import newton_interpolation_equidistant, newton_interpolation_divided_difference
from backend.numerical_methods.horner_table.change_variables import change_variables
from backend.numerical_methods.interpolation.central import bessel_interpolation, central_gauss_i, central_gauss_ii, stirlin_interpolation
from pprint import pprint
if __name__ == "__main__":
    x_nodes = [1.6, 1.8, 2.0, 2.2, 2.4]
    y_nodes = [4.23, 3.67, 2.99, 1.24, 0.87]

    #Tính bảng sai phân
    finite_differences_table = finite_differences(x_nodes, y_nodes)["finite_difference_table"]
    #Lấy gia trị sai phân Newton tiến
    f_coeff = [finite_differences_table[i][i+1] for i in range(len(finite_differences_table))]

    #Tính t_0
    t_0 = (4 - 4.23)/f_coeff[1]
    print(t_0)
    t = t_0
    t_prev = t_0+100
    count = 0

    # Xây dựng điều kiện dừng, lặp đến khi hội tụ
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
    # Chuyển đổi về giá trị x
    x= 0.2*t+1.6
    print(x)
    print(count)

    coeffs = newton_interpolation_equidistant(x_nodes, y_nodes)['forward_interpolation']['polynomial_coeffs_x']
    result = synthetic_division(coeffs, x)['value']
    print(result)
    print(t_0)
    print(f_coeff[1])
    """

    x_nodes = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
    y_nodes = [2.2074, 2.036, 1.7802, 1.4378, 1.0072, 0.4875, -0.1221, -0.8217]
    result = bessel_interpolation(x_nodes, y_nodes)
    # In ra các kết quả của result cho dễ nhìn
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{key}:")
            pprint(value)
            print("-" * 40)
    else:
        pprint(result)

    print(synthetic_division(result['bessel_polynomial_coeffs_u'], (1.43-1.3)/0.1-0.5)['value'])
    print(synthetic_division(result['bessel_polynomial_coeffs_t'], (1.43-1.3)/0.1)['value'])
    print(synthetic_division(result['bessel_polynomial_coeffs_x'], 1.43)['value'])
    """
