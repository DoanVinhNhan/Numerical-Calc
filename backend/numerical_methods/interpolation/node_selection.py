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
    
    - 'right' (Newton Tiến): Tìm mốc x_i <= x_bar gần nhất, lấy k mốc từ đó tiến lên.
    - 'left' (Newton Lùi): Tìm mốc x_i >= x_bar gần nhất, lấy k mốc từ đó lùi lại.
    - 'both' (Trung tâm): Lấy k mốc cân bằng nhất xung quanh x_bar.
    """
    try:
        df = pd.read_csv(
            file_stream,
            header=None,
            usecols=[0, 1],
            names=['x', 'y']
        )
    except pd.errors.ParserError:
        raise ValueError("File CSV không hợp lệ. Không thể phân tích dữ liệu.")
    except Exception as e:
        raise ValueError(f"Lỗi khi đọc file: {e}")

    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna().sort_values(by='x').reset_index(drop=True)

    if df.empty:
        raise ValueError("File CSV không chứa dữ liệu số hợp lệ ở 2 cột đầu tiên.")

    # --- Xử lý mốc trùng lặp ---
    warning_message = None
    duplicate_rows = df[df.duplicated(subset=['x'], keep=False)]
    
    if not duplicate_rows.empty:
        duplicate_x_values = sorted(duplicate_rows['x'].unique())
        warning_message = (
            f"CẢNH BÁO: Dữ liệu chứa các mốc x bị lặp lại. "
            f"Đã tự động loại bỏ các mốc trùng lặp, chỉ giữ lại mốc xuất hiện đầu tiên. "
            f"Các mốc bị lặp: {', '.join(map(str, duplicate_x_values))}"
        )
        df = df.drop_duplicates(subset=['x'], keep='first').reset_index(drop=True)

    total_valid_nodes = len(df)
    if num_nodes > total_valid_nodes:
        raise ValueError(f"Số mốc yêu cầu ({num_nodes}) lớn hơn số điểm dữ liệu hợp lệ và *không trùng lặp* ({total_valid_nodes}).")
    if num_nodes < 2:
        raise ValueError("Số mốc nội suy phải lớn hơn hoặc bằng 2.")

    # --- LOGIC CHỌN MỐC CHUẨN XÁC ---
    
    selected_df = pd.DataFrame()
    method_description = ""
    start_idx = 0
    end_idx = 0

    if method == 'right':
        # "Lân cận phải" (cho Newton Tiến):
        # 1. Tìm mốc x_i <= x_bar GẦN NHẤT. Đây là mốc x_0 lý tưởng.
        nodes_left = df[df['x'] <= x_bar]
        if not nodes_left.empty:
            start_node_idx = nodes_left['x'].idxmax()
        else:
            # Nếu tất cả các mốc đều > x_bar, ta phải lấy mốc đầu tiên.
            start_node_idx = df.index[0]
            
        # 2. Lấy k mốc từ mốc đó
        start_idx = start_node_idx
        end_idx = min(total_valid_nodes, start_idx + num_nodes)
        
        # 3. Điều chỉnh nếu không đủ k mốc (bị chạm biên phải): lùi start_idx lại
        if end_idx - start_idx < num_nodes:
            start_idx = max(0, end_idx - num_nodes)
            
        method_description = f"Trích xuất {num_nodes} mốc cho Newton Tiến (x̄ gần mốc đầu)"

    elif method == 'left':
        # "Lân cận trái" (cho Newton Lùi):
        # 1. Tìm mốc x_i >= x_bar GẦN NHẤT. Đây là mốc x_n lý tưởng.
        nodes_right = df[df['x'] >= x_bar]
        if not nodes_right.empty:
            end_node_idx = nodes_right['x'].idxmin()
        else:
            # Nếu tất cả các mốc đều < x_bar, ta phải lấy mốc cuối cùng.
            end_node_idx = df.index[-1]

        # 2. Lấy k mốc đến mốc đó
        end_idx = end_node_idx + 1 # +1 vì iloc không bao gồm mốc cuối
        start_idx = max(0, end_idx - num_nodes)
        
        # 3. Điều chỉnh nếu không đủ k mốc (bị chạm biên trái): tiến end_idx lên
        if end_idx - start_idx < num_nodes:
            end_idx = min(total_valid_nodes, start_idx + num_nodes)
            
        method_description = f"Trích xuất {num_nodes} mốc cho Newton Lùi (x̄ gần mốc cuối)"

    else: # method == 'both' (Lân cận 2 phía - Dùng cho Stirling/Bessel/Lagrange)
        # 1. Tìm mốc gần x_bar nhất
        df['dist'] = (df['x'] - x_bar).abs()
        closest_idx = df['dist'].idxmin()
        
        # 2. Lấy cân bằng 2 bên
        num_left = (num_nodes - 1) // 2
        num_right = num_nodes - 1 - num_left
        
        start_idx = max(0, closest_idx - num_left)
        end_idx = min(total_valid_nodes, closest_idx + num_right + 1)
        
        # 3. Điều chỉnh nếu bị chạm biên (lấy bù về phía còn lại)
        if end_idx == total_valid_nodes: # Chạm biên phải
            start_idx = max(0, total_valid_nodes - num_nodes)
        elif start_idx == 0: # Chạm biên trái
            end_idx = min(total_valid_nodes, num_nodes)
            
        method_description = f"Trích xuất {num_nodes} mốc lân cận cân bằng nhất với {x_bar}"

    selected_df = df.iloc[start_idx:end_idx].copy()

    return {
        "status": "success",
        "warning_message": warning_message,
        "method_description": method_description,
        "x_bar": x_bar,
        "num_nodes_found": len(selected_df),
        "selected_x": selected_df['x'].tolist(),
        "selected_y": selected_df['y'].tolist()
    }