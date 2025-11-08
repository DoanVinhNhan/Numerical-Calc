# backend/numerical_methods/interpolation/node_selection.py
import pandas as pd
import numpy as np
import io
from typing import List, Dict, Any

def select_interpolation_nodes(
    file_stream: io.BytesIO,
    x_bar: float,
    num_nodes: int,
    method: str
) -> Dict[str, Any]:
    """
    Trích xuất k mốc nội suy từ file CSV dựa trên giá trị x_bar và phương pháp.
    Tự động phát hiện, cảnh báo và loại bỏ các mốc x trùng lặp.
    """
    try:
        # Đọc file CSV, giả định 2 cột đầu tiên là x, y và không có header
        df = pd.read_csv(
            file_stream, 
            header=None, 
            usecols=[0, 1], 
            names=['x', 'y'],
            comment=',' # Bỏ qua các dòng chú thích/header nếu có
        )
    except pd.errors.ParserError:
        raise ValueError("File CSV không hợp lệ. Không thể phân tích dữ liệu.")
    except Exception as e:
        raise ValueError(f"Lỗi khi đọc file: {e}")

    # Chuyển đổi sang kiểu số và loại bỏ các dòng không hợp lệ, sắp xếp
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna().sort_values(by='x').reset_index(drop=True)

    if df.empty:
        raise ValueError("File CSV không chứa dữ liệu số hợp lệ ở 2 cột đầu tiên.")

    # --- BẮT ĐẦU SỬA ĐỔI: Xử lý mốc trùng lặp ---
    
    # 1. Phát hiện mốc x trùng lặp
    warning_message = None
    duplicate_rows = df[df.duplicated(subset=['x'], keep=False)]
    
    if not duplicate_rows.empty:
        duplicate_x_values = sorted(duplicate_rows['x'].unique())
        # 2. Tạo thông báo cảnh báo
        warning_message = (
            f"CẢNH BÁO: Dữ liệu chứa các mốc x bị lặp lại. "
            f"Đã tự động loại bỏ các mốc trùng lặp, chỉ giữ lại mốc xuất hiện đầu tiên. "
            f"Các mốc bị lặp: {', '.join(map(str, duplicate_x_values))}"
        )
        
        # 3. Loại bỏ mốc trùng lặp, giữ lại mốc đầu tiên
        df = df.drop_duplicates(subset=['x'], keep='first').reset_index(drop=True)

    # 4. Kiểm tra số lượng mốc *sau khi* đã loại bỏ trùng lặp
    if num_nodes > len(df):
        raise ValueError(f"Số mốc yêu cầu ({num_nodes}) lớn hơn số điểm dữ liệu hợp lệ và *không trùng lặp* ({len(df)}).")
    
    # Thêm kiểm tra số mốc tối thiểu
    if num_nodes < 2:
        raise ValueError("Số mốc nội suy phải lớn hơn hoặc bằng 2.")

    # --- KẾT THÚC SỬA ĐỔI ---
    
    selected_df = pd.DataFrame()
    method_description = ""

    if method == 'left':
        # Lấy `num_nodes` mốc cuối cùng có x <= x_bar
        left_nodes = df[df['x'] <= x_bar]
        if len(left_nodes) < num_nodes:
            raise ValueError(f"Không tìm thấy đủ {num_nodes} mốc ở bên trái (<= {x_bar}). Chỉ tìm thấy {len(left_nodes)} mốc.")
        selected_df = left_nodes.nlargest(num_nodes, 'x')
        method_description = f"Trích xuất {num_nodes} mốc bên trái (x <= {x_bar})"
    
    elif method == 'right':
        # Lấy `num_nodes` mốc đầu tiên có x >= x_bar
        right_nodes = df[df['x'] >= x_bar]
        if len(right_nodes) < num_nodes:
            raise ValueError(f"Không tìm thấy đủ {num_nodes} mốc ở bên phải (>= {x_bar}). Chỉ tìm thấy {len(right_nodes)} mốc.")
        selected_df = right_nodes.nsmallest(num_nodes, 'x')
        method_description = f"Trích xuất {num_nodes} mốc bên phải (x >= {x_bar})"
    
    else: # method == 'both'
        # Lấy `num_nodes` mốc gần nhất với x_bar
        df['dist'] = (df['x'] - x_bar).abs()
        selected_df = df.nsmallest(num_nodes, 'dist')
        method_description = f"Trích xuất {num_nodes} mốc gần nhất với {x_bar}"

    # Sắp xếp lại kết quả cuối cùng theo x
    selected_df = selected_df.sort_values(by='x')

    return {
        "status": "success",
        "warning_message": warning_message, # --- THÊM TRƯỜNG MỚI ---
        "method_description": method_description,
        "x_bar": x_bar,
        "num_nodes_found": len(selected_df),
        "selected_x": selected_df['x'].tolist(),
        "selected_y": selected_df['y'].tolist()
    }