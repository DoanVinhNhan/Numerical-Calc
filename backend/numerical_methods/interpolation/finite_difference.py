#backend/numerical_methods/interpolation/finite_difference.py
import numpy as np
def finite_differences(x_nodes, y_nodes):
    """
    Tính bảng sai phân hữu hạn cho các điểm (x_i, y_i) với các mốc x_i cách đều nhau.
    Parameters:
        x_nodes (list of float): Các điểm x_i.
        y_nodes (list of float): Các điểm y_i tương ứng.
    Returns:
        dict: Chứa bảng sai phân.
    """
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)

    if len(x_nodes) != len(y_nodes):
        raise ValueError("Số lượng mốc x và giá trị y phải bằng nhau.")
    n = len(x_nodes)
    if n == 0:
        return {
            "finite_difference_table": [],
            "steps": []
        }
    for i in range(n):
        if np.sum(np.isclose(x_nodes[i], x_nodes)) > 1:
            raise ValueError(f"Các mốc x phải phân biệt nhau. Mốc x={x_nodes[i]} bị lặp lại.")
    h = x_nodes[1] - x_nodes[0]
    for i in range(1, n-1):
        if not np.isclose(x_nodes[i+1] - x_nodes[i], h):
            raise ValueError("Các mốc x phải cách đều nhau.")

    # Khởi tạo bảng sai phân 
    table = np.zeros((n, n+1), dtype=float)
    table[:, 0] = x_nodes
    table[:, 1] = y_nodes

    # Tính các cột tiếp theo trong bảng sai phân
    for j in range(2, n + 1):
        for i in range(j-1, n):
            table[i, j] = table[i, j - 1] - table[i - 1, j - 1]
    return {
        "finite_difference_table": table.tolist()
        }