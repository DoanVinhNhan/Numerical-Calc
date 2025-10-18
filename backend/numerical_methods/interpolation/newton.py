#backend/numerical_methods/interpolation/newton.py
import numpy as np
from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
from backend.numerical_methods.interpolation.finite_difference import finite_differences
from backend.numerical_methods.interpolation.divided_difference import divided_differences
from backend.numerical_methods.horner_table.change_variables import change_variables
#Nội suy newton mốc cách đều
def newton_interpolation_equidistant(x_nodes, y_nodes):
    """
    Đa thức nội suy Newton dựa trên các điểm (x_i, y_i) với các mốc x_i cách đều nhau.
    Pn(x) = y_0 + f[x_0,x_1](x-x_0) + f[x_0,x_1,x_2](x-x_0)(x-x_1) + ... + f[x_0,x_1,...,x_n](x-x_0)(x-x_1)...(x-x_{n-1})
    Pn(t) = y_0 + Δy_0 t + Δ^2y_0 t(t-1)/2! + ... + Δ^n y_0 t(t-1)(t-2)...(t-n+1)/n!
    Trong đó: f[x_i,x_j,...,x_k] là tỷ sai phân.
              t = (x - x_0)/h với h là khoảng cách giữa các mốc x_i.
              x0 là mốc bên trái nếu dùng Newton tiến, x0 là mốc bên phải nếu dùng Newton lùi.
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
            "polynomial_coeffs_forward": [],
            "polynomial_coeffs_backward": [],
            "finite_difference_table": []
        }
    for i in range (n):
        if np.sum(np.isclose(x_nodes[i], x_nodes)) > 1:
            raise ValueError(f"Các mốc x phải phân biệt nhau. Mốc x={x_nodes[i]} bị lặp lại.")
    h = x_nodes[1] - x_nodes[0]
    for i in range(1, n-1):
        if not np.isclose(x_nodes[i+1] - x_nodes[i], h):
            raise ValueError("Các mốc x phải cách đều nhau.")
    
    # Bảng sai phân
    finite_diff_result = finite_differences(x_nodes, y_nodes)
    finite_diff_table = finite_diff_result['finite_difference_table']

    # Lấy các sai phân trên đường chéo (Newton tiến)
    finite_diffs_forward = [finite_diff_table[i][i+1] for i in range(n)]
    # Lấy các sai phân trên hàng cuối (Newton lùi)
    finite_diffs_backward = [finite_diff_table[n-1][i+1] for i in range(n)]

    # Đổi biến Newton tiến
    t_nodes_forward = (x_nodes - x_nodes[0]) / h
    # Đổi biến Newton lùi
    t_nodes_backward = (x_nodes - x_nodes[-1]) / h
    t_nodes_backward = t_nodes_backward[::-1]

    # Bảng tích w_i(x) tiến
    w_forward = []
    w_coeffs_forward = [1.0]
    w_forward.append(w_coeffs_forward.copy())
    for i in range(n-1):
        new_w_result = reverse_horner(w_coeffs_forward, t_nodes_forward[i])
        w_coeffs_forward = new_w_result['coeffs']
        w_forward.append(w_coeffs_forward.copy())
    w_forward = [[0.0]*(len(w_forward)-i-1)+w_forward[i] for i in range(len(w_forward))]

    # Bảng tích w_i(x) lùi
    w_backward = []
    w_coeffs_backward = [1.0]
    w_backward.append(w_coeffs_backward.copy())
    for i in range(n-1):
        new_w_result = reverse_horner(w_coeffs_backward, t_nodes_backward[i])
        w_coeffs_backward = new_w_result['coeffs']
        w_backward.append(w_coeffs_backward.copy())
    w_backward = [[0.0]*(len(w_backward)-i-1)+w_backward[i] for i in range(len(w_backward))]

    #Tính hệ số (sai phân chia cho giai thừa)
    coeffs_forward = [finite_diffs_forward / np.math.factorial(i) for i, finite_diffs_forward in enumerate(finite_diffs_forward)]
    coeffs_backward = [finite_diffs_backward / np.math.factorial(i) for i, finite_diffs_backward in enumerate(finite_diffs_backward)]

    # Tính đa thức nội suy Newton tiến
    newton_forward_coeffs_t = np.array(coeffs_forward)@np.array(w_forward)
    # Tính đa thức nội suy Newton lùi
    newton_backward_coeffs_t = np.array(coeffs_backward)@np.array(w_backward)
    # Đổi biến trở lại hệ số đa thức theo x
    newton_forward_coeffs = change_variables(newton_forward_coeffs_t.tolist(), a=h, b=x_nodes[0])['variables_coeffs']
    newton_backward_coeffs = change_variables(newton_backward_coeffs_t.tolist(), a=h, b=x_nodes[-1])['variables_coeffs']


    return {
        "finite_difference_table": finite_diff_table,
        "h": h,
        "forward_interpolation": {
            "start_node": x_nodes[0],
            "diffs": finite_diffs_forward,
            "coeffs_scaled": coeffs_forward,
            "w_polynomials_t": w_forward,
            "polynomial_coeffs_t": newton_forward_coeffs_t.tolist(),
            "polynomial_coeffs_x": newton_forward_coeffs
        },
        "backward_interpolation": {
            "start_node": x_nodes[-1],
            "diffs": finite_diffs_backward,
            "coeffs_scaled": coeffs_backward,
            "w_polynomials_t": w_backward,
            "polynomial_coeffs_t": newton_backward_coeffs_t.tolist(),
            "polynomial_coeffs_x": newton_backward_coeffs
        }
    }

#Nội suy newton mốc bất kỳ
def newton_interpolation_divided_difference(x_nodes, y_nodes):
    """
    Đa thức nội suy Newton dựa trên các điểm (x_i, y_i) với các mốc x_i không cần cách đều nhau.
    Pn(x) = y_0 + f[x_0,x_1](x-x_0) + f[x_0,x_1,x_2](x-x_0)(x-x_1) + ... + f[x_0,x_1,...,x_n](x-x_0)(x-x_1)...(x-x_{n-1})
    Trong đó: f[x_i,x_j,...,x_k] là tỷ sai phân.
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
            "finite_difference_table": []
        }
    for i in range (n):
        if np.sum(np.isclose(x_nodes[i], x_nodes)) > 1:
            raise ValueError(f"Các mốc x phải phân biệt nhau. Mốc x={x_nodes[i]} bị lặp lại.")

    # Sắp xếp các mốc x và y tương ứng
    sorted_indices = np.argsort(x_nodes)
    x_nodes = x_nodes[sorted_indices]
    y_nodes = y_nodes[sorted_indices]

    # Bảng tỷ sai phân
    divided_difference_result = divided_differences(x_nodes, y_nodes)
    divided_difference_table = divided_difference_result['divided_difference_table']

    # Lấy các tỷ sai phân trên đường chéo (Newton Tiến)
    divided_diffs_forward = [divided_difference_table[i][i+1] for i in range(n)]
    # Lấy các tỷ sai phân trên hàng cuối (Newton Lùi)
    divided_diffs_backward = [divided_difference_table[n-1][i+1] for i in range(n)]

    # Bảng tích w_i(x) tiến
    w_forward = []
    w_coeffs_forward = [1.0]
    w_forward.append(w_coeffs_forward.copy())
    for i in range(n-1):
        new_w_result = reverse_horner(w_coeffs_forward, x_nodes[i])
        w_coeffs_forward = new_w_result['coeffs']
        w_forward.append(w_coeffs_forward.copy())
    w_forward = [[0.0]*(len(w_forward)-i-1)+w_forward[i] for i in range(len(w_forward))]

    #Bảng tích w_i(x) lùi
    w_backward = []
    w_coeffs_backward = [1.0]
    w_backward.append(w_coeffs_backward.copy())
    for i in range(n-1):
        new_w_result = reverse_horner(w_coeffs_backward, x_nodes[-(i+1)])
        w_coeffs_backward = new_w_result['coeffs']
        w_backward.append(w_coeffs_backward.copy())
    w_backward = [[0.0]*(len(w_backward)-i-1)+w_backward[i] for i in range(len(w_backward))]

    #Hệ số đa thức nội suy Newton tiến
    coeffs_forward = np.array(divided_diffs_forward)@np.array(w_forward)
    #Hệ số đa thức nội suy Newton lùi
    coeffs_backward = np.array(divided_diffs_backward)@np.array(w_backward)

    return {
        "divided_difference_table": divided_difference_table,
        "x_nodes_sorted": x_nodes.tolist(),
        "y_nodes_sorted": y_nodes.tolist(),
        "forward_interpolation": {
            "start_node": x_nodes[0],
            "diffs": divided_diffs_forward,
            "coeffs_scaled": coeffs_forward,
            "w_polynomials_t": w_forward,
            "polynomial_coeffs": coeffs_forward.tolist(),
        },
        "backward_interpolation": {
            "start_node": x_nodes[-1],
            "diffs": divided_diffs_backward,
            "coeffs_scaled": coeffs_backward,
            "w_polynomials_t": w_backward,
            "polynomial_coeffs": coeffs_backward.tolist(),
        }
    }
