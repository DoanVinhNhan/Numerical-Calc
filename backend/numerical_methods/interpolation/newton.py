#backend/numerical_methods/interpolation/newton.py
import numpy as np
from backend.numerical_methods.horner_table.all_derivatives import all_derivatives
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
from backend.numerical_methods.horner_table.w_function import calculate_w_function


#Nội suy newton mốc cách đều
def newton_interpolation_equidistant(x_nodes, y_nodes):
    """
    Đa thức nội suy Newton dựa trên các điểm (x_i, y_i) với các mốc x_i cách đều nhau.
    Pn(x) = y_0 + f[x_0,x_1](x-x_0) + f[x_0,x_1,x_2](x-x_0)(x-x_1) + ... + f[x_0,x_1,...,x_n](x-x_0)(x-x_1)...(x-x_{n-1})
    Trong đó, f[x_i,x_j,...,x_k] là tỷ sai phân.
    Parameters:
        x_nodes (list of float): Các điểm x_i.
        y_nodes (list of float): Các điểm y_i tương ứng.
    Returns:
        dict: Chứa các bước tính toán và đa thức kết quả.
    """
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)
    if len(x_nodes) != len(y_nodes):
        raise ValueError("Số lượng mốc x và giá trị y phải bằng nhau.")
    n = len(x_nodes)
    if n == 0:
        return {
            "polynomial_coeffs": [],
            "steps": []
        }
    for i in range (n):
        if np.sum(np.isclose(x_nodes[i], x_nodes)) > 1:
            raise ValueError(f"Các mốc x phải phân biệt nhau. Mốc x={x_nodes[i]} bị lặp lại.")
    h = x_nodes[1] - x_nodes[0]
    for i in range(1, n-1):
        if not np.isclose(x_nodes[i+1] - x_nodes[i], h):
            raise ValueError("Các mốc x phải cách đều nhau.")

#Nội suy newton mốc bất kỳ