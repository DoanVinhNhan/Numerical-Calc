#!/usr/bin/env python3
import os

def print_tree(directory, prefix="", max_depth=4, current_depth=0):
    """In cấu trúc thư mục dưới dạng tree"""
    if current_depth >= max_depth:
        return
    
    items = sorted(os.listdir(directory))
    # Lọc bỏ các thư mục không cần thiết
    items = [item for item in items if not item.startswith('.') and item != '__pycache__']
    
    for i, item in enumerate(items):
        path = os.path.join(directory, item)
        is_last = i == len(items) - 1
        
        # In tên file/thư mục
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{item}")
        
        # Nếu là thư mục, tiếp tục đệ quy
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            print_tree(path, prefix + extension, max_depth, current_depth + 1)

if __name__ == "__main__":
    print("📁 Cấu trúc thư mục dự án Numerical-Calc")
    print("=" * 50)
    print("refactor_src/")
    print_tree(".", max_depth=5)