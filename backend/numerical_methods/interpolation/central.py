# backend/numerical_methods/interpolation/central.py
import numpy as np
from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
from backend.numerical_methods.interpolation.finite_difference import finite_differences
from backend.numerical_methods.interpolation.divided_difference import divided_differences
from backend.numerical_methods.horner_table.change_variables import change_variables

def central_gauss_i(x_nodes, y_nodes):
    """
    Nội suy trung tâm Gauss I cho các điểm (x_i, y_i) với các mốc x_i cách đều nhau.
    Số mốc lẻ, xuất phát từ mốc chính giữa.
    Kết nạp bên phải trước, xen kẽ P,T,P,T,...
    P(x)=a_0+a_1(x-x0)+a_2(x-x0)(x-x1)+a_3(x-x0)(x-x1)(x-x_{-1})+a_4(x-x0)(x-x1)(x-x_{-1})(x-x_{2})...

    a_{2i}=\delta^{2i} y_{-i} / (2i)!h^{2i}
    a_{2i+1}=\delta^{2i+1} y_{-i} / (2i+1)!h^{2i+1}

    P(x_0+th)=y_0+t\delta y_0 + \frac{\delta^2 y_{-1}}{2!} t(t-1) + \frac{\delta^3 y_{-1}}{3!} t(t-1)(t+1) + ...
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
    h = x_nodes[1] - x_nodes[0]
    for i in range(1, n-1):
        if not np.isclose(x_nodes[i+1] - x_nodes[i], h):
            raise ValueError("Các mốc x phải cách đều nhau.")
    if n % 2 == 0:
        raise ValueError("Phương pháp Gauss I yêu cầu số mốc x là lẻ.")
    
    # Bảng sai phân
    finite_diff_result = finite_differences(x_nodes, y_nodes)
    finite_diff_table = finite_diff_result['finite_difference_table']
    # Lấy các sai phân trung tâm
    central_finite_diffs = []
    start_row = (n-1)//2

    for j in range(1,n+1):
        i = start_row + (j // 2) 
        if (i < n and j < len(finite_diff_table[i])):
                central_finite_diffs.append(finite_diff_table[i][j])
        else:
            break
    # Đổi biến
    t_nodes = (x_nodes - x_nodes[start_row]) / h

    # Bảng tích w_i(t)
    w = []
    w_coeffs = [1.0]
    w.append(w_coeffs.copy())
    for i in range((n-1)//2):
        new_w_result = reverse_horner(w_coeffs, t_nodes[start_row - i])
        w_coeffs = new_w_result['coeffs']
        w.append(w_coeffs.copy())
        new_w_result = reverse_horner(w_coeffs, t_nodes[start_row + i +1])
        w_coeffs = new_w_result['coeffs']
        w.append(w_coeffs.copy())
    w = [[0.0]*(len(w)-i-1)+w[i] for i in range(len(w))]

    # Hệ số c_{2i}, c_{2i+1}
    c_coeffs = []
    for i in range(len(central_finite_diffs)):
        c_coeffs.append(central_finite_diffs[i] / np.math.factorial(i))

    # Tính đa thức nội suy Gauss I theo biến t
    gauss_i_polynomial_t = np.array(c_coeffs)@np.array(w)

    # Tính đa thức nội suy Gauss I theo biến x
    gauss_i_polynomial_x = change_variables(gauss_i_polynomial_t, a=h, b=x_nodes[start_row])['variables_coeffs']
    return {
        "start_node": x_nodes[start_row],
        "h": h,
        "t_nodes": t_nodes.tolist(),
        "finite_difference_table": finite_diff_table,
        "central_finite_diffs": central_finite_diffs,
        "c_coeffs": c_coeffs,
        "w_table": w,
        "polynomial_coeffs_t": gauss_i_polynomial_t.tolist(),
        "polynomial_coeffs_x": gauss_i_polynomial_x,
    }

def central_gauss_ii(x_nodes, y_nodes):
    """
    Nội suy trung tâm Gauss II cho các điểm (x_i, y_i) với các mốc x_i cách đều nhau.
    Số mốc lẻ, xuất phát từ mốc chính giữa.
    Kết nạp bên trái trước, xen kẽ T,P,T,P,...
    P(x)=a_0+a_1(x-x_0)+a_2(x-x_0)(x-x_{-1})+a_3(x-x_0)(x-x_{-1})(x-x_1)+a_4(x-x_0)(x-x_{-1})(x-x_1)(x-x_{2})...

    a_{2i-1}=\delta^{2i-1} y_{-i} / (2i-1)!h^{2i-1}
    a_{2i}=\delta^{2i} y_{-i} / (2i)!h^{2i}

    P(x_0+th)=y_0+t\delta y_{-1} + \frac{\delta^2 y_{-1}}{2!} t(t+1) + \frac{\delta^3 y_{-2}}{3!} t(t+1)(t-1) + ...
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
    h = x_nodes[1] - x_nodes[0]
    for i in range(1, n-1):
        if not np.isclose(x_nodes[i+1] - x_nodes[i], h):
            raise ValueError("Các mốc x phải cách đều nhau.")
    if n % 2 == 0:
        raise ValueError("Phương pháp Gauss II yêu cầu số mốc x là lẻ.")
    
    # Bảng sai phân
    finite_diff_result = finite_differences(x_nodes, y_nodes)
    finite_diff_table = finite_diff_result['finite_difference_table']
    # Lấy các sai phân trung tâm
    central_finite_diffs = []
    start_row = (n-1)//2

    for j in range(1,n+1):
        i = start_row + (j-1) // 2
        if (i < n and j < len(finite_diff_table[i])):
                central_finite_diffs.append(finite_diff_table[i][j])
        else:
            break
    # Đổi biến
    t_nodes = (x_nodes - x_nodes[start_row]) / h

    # Bảng tích w_i(t)
    w = []
    w_coeffs = [1.0]
    w.append(w_coeffs.copy())
    for i in range((n-1)//2):
        new_w_result = reverse_horner(w_coeffs, t_nodes[start_row + i])
        w_coeffs = new_w_result['coeffs']
        w.append(w_coeffs.copy())
        new_w_result = reverse_horner(w_coeffs, t_nodes[start_row - i - 1])
        w_coeffs = new_w_result['coeffs']
        w.append(w_coeffs.copy())
    w = [[0.0]*(len(w)-i-1)+w[i] for i in range(len(w))]

    # Hệ số c_{2i}, c_{2i+1}
    c_coeffs = []
    for i in range(len(central_finite_diffs)):
        c_coeffs.append(central_finite_diffs[i] / np.math.factorial(i))
    
    # Tính đa thức nội suy Gauss II theo biến t
    gauss_ii_polynomial_t = np.array(c_coeffs)@np.array(w)
    # Tính đa thức nội suy Gauss II theo biến x
    gauss_ii_polynomial_x = change_variables(gauss_ii_polynomial_t, a=h, b=x_nodes[start_row])['variables_coeffs']

    return {
        "start_node": x_nodes[start_row],
        "h": h,
        "t_nodes": t_nodes.tolist(),
        "finite_difference_table": finite_diff_table,
        "central_finite_diffs": central_finite_diffs,
        "c_coeffs": c_coeffs,
        "w_table": w,
        "polynomial_coeffs_t": gauss_ii_polynomial_t.tolist(),
        "polynomial_coeffs_x": gauss_ii_polynomial_x,
    }

def stirlin_interpolation(x_nodes, y_nodes):
    """Nội suy Stirlin cho các điểm (x_i, y_i) với các mốc x_i cách đều nhau.
       Số mốc lẻ, xuất phát từ mốc chính giữa.
       Stirlin = Gauss I + Gauss II / 2
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
    h = x_nodes[1] - x_nodes[0]
    for i in range(1, n-1):
        if not np.isclose(x_nodes[i+1] - x_nodes[i], h):
            raise ValueError("Các mốc x phải cách đều nhau.")
    if n % 2 == 0:
        raise ValueError("Phương pháp Stirlin yêu cầu số mốc x là lẻ.")
    
    # Bảng sai phân
    finite_diff_result = finite_differences(x_nodes, y_nodes)
    finite_diff_table = finite_diff_result['finite_difference_table']

    # Lấy các sai phân trung tâm của Gauss I
    central_finite_diffs_i = []
    start_row = (n-1)//2

    for j in range(1,n+1):
        i = start_row + (j // 2)
        if (i < n and j < len(finite_diff_table[i])):
                central_finite_diffs_i.append(finite_diff_table[i][j])
        else:
            break
    # Lấy các sai phân trung tâm của Gauss II
    central_finite_diffs_ii = []
    for j in range(1,n+1):
        i = start_row + (j -1) // 2
        if (i < n and j < len(finite_diff_table[i])):
                central_finite_diffs_ii.append(finite_diff_table[i][j])
        else:
            break
    # Tính hệ số sai phân trung tâm của Stirlin
    central_finite_diffs = []
    for i in range(len(central_finite_diffs_i)):
        central_finite_diffs.append( (central_finite_diffs_i[i] + central_finite_diffs_ii[i]) / 2 )

    # Đổi biến
    t_nodes = (x_nodes - x_nodes[start_row]) / h

    return