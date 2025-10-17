#backend/numerical_methods/interpolation/newton.py
import numpy as np
from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
from backend.numerical_methods.interpolation.finite_difference import finite_differences

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
    finite_diff_result = finite_differences(y_nodes, h)
    finite_diff_table = finite_diff_result['finite_difference_table']

    # Lấy các sai phân trên đường chéo (Newton tiến)
    finite_diffs_forward = [finite_diff_table[i][i+1] for i in range(n)]
    # Lấy các sai phân trên hàng cuối (Newton lùi)
    finite_diffs_backward = [finite_diff_table[n-1][i+1] for i in range(n)]

    # Đổi biến Newton tiến
    t_nodes_forward = (x_nodes - x_nodes[0]) / h
    # Đổi biến Newton lùi
    t_nodes_backward = (x_nodes - x_nodes[-1]) / h

    # Danh sách các w_i(x) tiến
    w_forward = []
    w_coeffs_forward = [0.0]*(n-1) + [1.0]
    w_forward.append(w_coeffs_forward.copy())
    for i in range(n):
        new_w_result = reverse_horner(w_coeffs_forward, t_nodes_forward[i])
        w_coeffs_forward = new_w_result['coeffs']
        w_forward.append(w_coeffs_forward.copy())
    

    # Danh sách các w_i(x) lùi
    w_backward = []
    w_coeffs_backward = [0.0]*(n-1) + [1.0]
    w_backward.append(w_coeffs_backward.copy())
    for i in range(n):
        new_w_result = reverse_horner(w_coeffs_backward, t_nodes_backward[i])
        w_coeffs_backward = [0.0]*(n-1) + new_w_result['coeffs']
        w_backward.append(w_coeffs_backward.copy())

    #Tính hệ số (sai phân cho giai thừa)
    coeffs_forward = [finite_diffs_forward / np.math.factorial(i) for i, finite_diffs_forward in enumerate(finite_diffs_forward)]
    coeffs_backward = [finite_diffs_backward / np.math.factorial(i) for i, finite_diffs_backward in enumerate(finite_diffs_backward)]

    # Tính đa thức nội suy Newton tiến
    newton_forward_coeffs_t = np.array(coeffs_forward)@np.array(w_forward)
    # Tính đa thức nội suy Newton lùi
    newton_backward_coeffs_t = np.array(coeffs_backward)@np.array(w_backward)
    # Đổi biến trở lại hệ số đa thức theo x


    return {
        "polynomial_coeffs_forward_t": newton_forward_coeffs_t.tolist(),
        "polynomial_coeffs_backward_t": newton_backward_coeffs_t.tolist(),
        "polynomial_coeffs_forward_x": newton_forward_coeffs.tolist(),
        "polynomial_coeffs_backward_x": newton_backward_coeffs.tolist(),
        "finite_difference_table": finite_diff_table
    }

#Nội suy newton mốc bất kỳ