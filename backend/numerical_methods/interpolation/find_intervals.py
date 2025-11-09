# backend/numerical_methods/interpolation/find_intervals.py
import pandas as pd
import numpy as np
import io
from typing import List, Dict, Any

def find_root_intervals(
    file_stream: io.BytesIO,
    y_bar: float,
    num_nodes: int,
    method: str = 'both'
) -> Dict[str, Any]:
    """
    Tìm các khoảng cách ly nghiệm f(x) = y_bar từ file CSV và mở rộng
    khoảng đó ra k mốc lân cận dựa trên phương pháp mở rộng được chọn.

    method: 'left' | 'right' | 'both' (mặc định 'both')
    """
    try:
        df = pd.read_csv(
            file_stream,
            header=None,
            usecols=[0, 1],
            names=['x', 'y']
        )
    except Exception as e:
        raise ValueError(f"Lỗi khi đọc file CSV: {e}")

    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna().sort_values(by='x').reset_index(drop=True)
    total_valid_nodes = len(df)

    if total_valid_nodes < 2:
        raise ValueError("Cần ít nhất 2 điểm dữ liệu để tìm khoảng cách ly.")
        
    if num_nodes < 2:
        raise ValueError("Số mốc nội suy (k) phải lớn hơn hoặc bằng 2.")
    if num_nodes > total_valid_nodes:
        raise ValueError(f"Số mốc yêu cầu ({num_nodes}) lớn hơn số điểm dữ liệu hợp lệ ({total_valid_nodes}).")

    # Xử lý mốc trùng lặp
    warning_message = None
    duplicate_rows = df[df.duplicated(subset=['x'], keep=False)]
    
    if not duplicate_rows.empty:
        duplicate_x_values = sorted(duplicate_rows['x'].unique())
        warning_message = (
            f"CẢNH BÁO: Dữ liệu chứa các mốc x bị lặp lại. "
            f"Đã tự động loại bỏ, chỉ giữ lại mốc đầu tiên. "
            f"Các mốc bị lặp: {', '.join(map(str, duplicate_x_values))}"
        )
        df = df.drop_duplicates(subset=['x'], keep='first').reset_index(drop=True)
        total_valid_nodes = len(df)
        if num_nodes > total_valid_nodes:
             raise ValueError(f"Số mốc yêu cầu ({num_nodes}) lớn hơn số điểm dữ liệu hợp lệ và *không trùng lặp* ({total_valid_nodes}).")

    # --- Logic tìm khoảng ---
    df['diff'] = df['y'] - y_bar
    # Bỏ qua các giá trị 0 (trường hợp nghiệm đúng tại mốc)
    df['sign'] = np.sign(df['diff']).replace(0, np.nan).ffill().bfill()
    
    # Tìm nơi dấu thay đổi (ví dụ: từ -1 sang 1 hoặc 1 sang -1)
    sign_changes = df['sign'].iloc[1:].values * df['sign'].iloc[:-1].values
    
    intervals = []
    found_interval_indices = set() # Dùng để tránh các khoảng bị trùng lặp

    # Lặp qua các vị trí có đổi dấu
    for i in np.where(sign_changes < 0)[0]:
        # Khoảng đổi dấu gốc là [i, i+1]
        
        # --- Logic mở rộng khoảng mới ---
        left_idx = i
        right_idx = i + 1
        current_nodes = 2
        
        sign_left = df['sign'].iloc[left_idx]
        sign_right = df['sign'].iloc[right_idx]

        can_expand_left = (left_idx > 0) and (method in ('left', 'both'))
        can_expand_right = (right_idx < total_valid_nodes - 1) and (method in ('right', 'both'))

        # Mở rộng xen kẽ 2 bên cho đến khi đủ k mốc hoặc bị chặn
        while current_nodes < num_nodes:
            if not can_expand_left and not can_expand_right:
                break # Dừng nếu không thể mở rộng cả 2 phía

            # 1. Thử mở rộng sang trái
            if can_expand_left:
                sign_next_left = df['sign'].iloc[left_idx - 1]
                if sign_next_left == sign_left:
                    # Hợp lệ: mốc mới cùng dấu, vẫn là khoảng cách ly
                    left_idx -= 1
                    current_nodes += 1
                    can_expand_left = (left_idx > 0)
                else:
                    # Không hợp lệ: mốc mới khác dấu, gặp nghiệm khác
                    can_expand_left = False
            
            if current_nodes >= num_nodes:
                break
                
            # 2. Thử mở rộng sang phải
            if can_expand_right:
                sign_next_right = df['sign'].iloc[right_idx + 1]
                if sign_next_right == sign_right:
                    # Hợp lệ
                    right_idx += 1
                    current_nodes += 1
                    can_expand_right = (right_idx < total_valid_nodes - 1)
                else:
                    # Không hợp lệ
                    can_expand_right = False
            
            # Nếu chỉ mở rộng một bên, khóa luôn cờ bên kia
            if method == 'left':
                can_expand_right = False
            elif method == 'right':
                can_expand_left = False
        
        # --- Kết thúc logic mở rộng ---

        # Tránh thêm trùng lặp
        if (left_idx, right_idx) not in found_interval_indices:
            found_interval_indices.add((left_idx, right_idx))
            selected_df = df.iloc[left_idx : right_idx + 1].copy()
            
            intervals.append({
                "interval_index": len(intervals) + 1,
                "selected_x": selected_df['x'].tolist(),
                "selected_y": selected_df['y'].tolist(),
                "original_interval": [df['x'].iloc[i], df['x'].iloc[i+1]],
                "num_nodes_found": len(selected_df)
            })

    method_text = ""
    if method == 'left':
        method_text = "về bên trái"
    elif method == 'right':
        method_text = "về bên phải"
    else:
        method_text = "về cả hai bên"

    if not intervals:
        method_description = f"Không tìm thấy khoảng cách ly nghiệm nào cho y = {y_bar}."
    else:
        method_description = f"Tìm thấy {len(intervals)} khoảng. Đã mở rộng {method_text} để lấy tối đa {num_nodes} mốc."

    return {
        "status": "success",
        "warning_message": warning_message,
        "method_description": method_description,
        "y_bar": y_bar,
        "num_intervals_found": len(intervals),
        "intervals": intervals,
        "all_x": df['x'].tolist(),
        "all_y": df['y'].tolist()
    }