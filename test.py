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
    coeffs_t = [1, 2, 3]  # Hệ số của đa thức theo biến t
    a = 2
    b = 1
    result_change = change_variables(coeffs_t, a, b)
    print("Kết quả đổi biến:", result_change)
