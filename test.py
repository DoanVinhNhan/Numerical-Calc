from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
import numpy as np
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.numerical_methods.interpolation.lagrange import lagrange_interpolation
from backend.numerical_methods.interpolation.divided_difference import divided_differences
from backend.numerical_methods.interpolation.finite_difference import finite_differences
from backend.numerical_methods.interpolation.newton import newton_interpolation_equidistant
from backend.numerical_methods.horner_table.change_variables import change_variables
if __name__ == "__main__":
    # Ví dụ sử dụng hàm change_variables
    frontward_t = [6.916666666665073e-05, -0.0003833333333331485, -0.009879166666667393, 0.04018333333333444, 0.4481099999999995, 0.5597]
    frontward = [2.21e-08, 5.48e-07, -8.03e-05, -0.00103, 0.0957, 1.5818]
    backward_t = [6.916666666665073e-05, 0.0013458333333331216, -0.0002541666666676559, -0.07904583333333527, 0.13348499999999855, 2.5465]
    backward = [2.21e-08, 3.86e-06, 0.00018, 0.00067, -0.0343, 2.3371]

    changed_frontward = change_variables(frontward_t, a=0.2, b=2.1)['variables_coeffs']
    changed_backward = change_variables(backward_t, a=0.2, b=3.1)['variables_coeffs']
    print(changed_frontward)
    print(changed_backward)