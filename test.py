import numpy as np
import matplotlib.pyplot as plt
import sys
import os
# Đảm bảo import đầy đủ các hàm từ sympy
from sympy import symbols, lambdify, sympify

# --- Thêm đường dẫn dự án ---
# Giả định test.py nằm ở thư mục gốc, cùng cấp với 'backend'
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --- Kết thúc ---

try:
    # Import các hàm Spline
    from backend.numerical_methods.interpolation.spline import (
        spline_linear, 
        spline_quadratic, 
        spline_cubic
    )
    # Import hàm Bình phương tối thiểu
    from backend.numerical_methods.interpolation.least_squares import (
        least_squares_approximation
    )
except ImportError as e:
    print(f"Lỗi Import: {e}")
    print("Không thể tìm thấy các module cần thiết.")
    print("Hãy đảm bảo bạn đã tạo các file sau:")
    print("  - backend/numerical_methods/interpolation/spline.py")
    print("  - backend/numerical_methods/interpolation/least_squares.py")
    print("...và đang chạy 'test.py' từ thư mục gốc của dự án.")
    sys.exit(1)

# --- Dữ liệu chung cho Spline (từ slide 18_Spline 20251.pdf) ---
spline_x_nodes = [0.3, 0.7, 1.2, 1.5, 1.8, 2.2, 2.6]
spline_y_nodes = [1.2, 2.7, 3.0, 2.3, 3.2, 1.0, 0.8]

def test_linear_spline_plot():
    """
    Kiểm tra và vẽ đồ thị cho hàm spline_linear.
    """
    print("\n--- Bắt đầu kiểm tra Spline Cấp 1 ---")
    try:
        result = spline_linear(spline_x_nodes, spline_y_nodes)
        if result["status"] != "success":
            print(f"Lỗi: {result.get('error')}")
            return

        print(f"Đã tính toán {result['n_segments']} đoạn spline cấp 1.")
        plt.figure(figsize=(10, 6))
        plt.plot(spline_x_nodes, spline_y_nodes, 'o', color='blue', markersize=8, label='Data Points')

        for i, segment in enumerate(result["splines"]):
            x_start, x_end = segment["interval"]
            a_k, b_k = segment["coeffs"]
            x_seg = np.linspace(x_start, x_end, 10)
            y_seg = a_k * x_seg + b_k
            plt.plot(x_seg, y_seg, 'r-', label='Spline Cấp 1' if i == 0 else None)

        plt.title('Kiểm tra Spline Tuyến tính (Cấp 1)')
        plt.xlabel('Trục X'); plt.ylabel('Trục Y')
        plt.legend(); plt.grid(True, linestyle='--', alpha=0.6)
        
        output_filename = 'test_spline_linear.png'
        plt.savefig(output_filename)
        print(f"Đã lưu đồ thị vào file: {output_filename}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

def test_quadratic_spline_plot():
    """
    Kiểm tra và vẽ đồ thị cho hàm spline_quadratic.
    """
    print("\n--- Bắt đầu kiểm tra Spline Cấp 2 ---")
    boundary_m1 = 0.0  # Điều kiện biên S'(x_0) = 0
    
    try:
        result = spline_quadratic(spline_x_nodes, spline_y_nodes, boundary_m1)
        if result["status"] != "success":
            print(f"Lỗi: {result.get('error')}")
            return
            
        print(f"Đã tính toán {result['n_segments']} đoạn spline cấp 2.")
        plt.figure(figsize=(10, 6))
        plt.plot(spline_x_nodes, spline_y_nodes, 'o', color='blue', markersize=8, label='Data Points')

        for i, segment in enumerate(result["splines"]):
            x_start, x_end = segment["interval"]
            a_k, b_k, c_k = segment["coeffs"]  # S(x) = ax^2 + bx + c
            x_seg = np.linspace(x_start, x_end, 50)
            y_seg = a_k * (x_seg**2) + b_k * x_seg + c_k
            plt.plot(x_seg, y_seg, 'g-', label='Spline Cấp 2' if i == 0 else None)

        plt.title("Kiểm tra Spline Bậc 2 (Cấp 2) với S'(x₀)=0")
        plt.xlabel('Trục X'); plt.ylabel('Trục Y')
        plt.legend(); plt.grid(True, linestyle='--', alpha=0.6)
        
        output_filename = 'test_spline_quadratic.png'
        plt.savefig(output_filename)
        print(f"Đã lưu đồ thị vào file: {output_filename}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

def test_cubic_spline_plot():
    """
    Kiểm tra và vẽ đồ thị cho hàm spline_cubic.
    """
    print("\n--- Bắt đầu kiểm tra Spline Cấp 3 ---")
    # Điều kiện biên: Spline Tự nhiên
    boundary_alpha_start = 0.0  # S''(x_0) = 0
    boundary_alpha_end = 0.0    # S''(x_n) = 0
    
    try:
        result = spline_cubic(spline_x_nodes, spline_y_nodes, boundary_alpha_start, boundary_alpha_end)
        if result["status"] != "success":
            print(f"Lỗi: {result.get('error')}")
            return
            
        print(f"Đã tính toán {result['n_segments']} đoạn spline cấp 3.")
        plt.figure(figsize=(10, 6))
        plt.plot(spline_x_nodes, spline_y_nodes, 'o', color='blue', markersize=8, label='Data Points')

        for i, segment in enumerate(result["splines"]):
            x_start, x_end = segment["interval"]
            x_k = segment["shift_point"]
            a_k, b_k, c_k, d_k = segment["coeffs"] # S(x) = a(t)^3 + b(t)^2 + c(t) + d, t = x - x_k
            
            x_seg = np.linspace(x_start, x_end, 50)
            t_seg = x_seg - x_k 
            y_seg = a_k * (t_seg**3) + b_k * (t_seg**2) + c_k * t_seg + d_k
            plt.plot(x_seg, y_seg, 'm-', label='Spline Cấp 3 (Tự nhiên)' if i == 0 else None)

        plt.title('Kiểm tra Spline Bậc 3 (Tự nhiên)')
        plt.xlabel('Trục X'); plt.ylabel('Trục Y')
        plt.legend(); plt.grid(True, linestyle='--', alpha=0.6)
        
        output_filename = 'test_spline_cubic.png'
        plt.savefig(output_filename)
        print(f"Đã lưu đồ thị vào file: {output_filename}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

def test_least_squares_simple_plot():
    """
    Kiểm tra LSQ với dữ liệu đường thẳng đơn giản.
    """
    print("\n--- Bắt đầu kiểm tra Bình phương tối thiểu (Đơn giản) ---")
    
    x_data = [1, 2, 3, 4]
    y_data = [2.1, 3.9, 6.1, 8.0]
    basis_funcs_str = ['1', 'x'] # g(x) = a_1 * 1 + a_2 * x
    
    print(f"Dữ liệu X: {x_data}")
    print(f"Dữ liệu Y: {y_data}")
    print(f"Hàm cơ sở: {basis_funcs_str}")

    try:
        result = least_squares_approximation(x_data, y_data, basis_funcs_str)
        if result["status"] != "success":
            print(f"Lỗi: {result.get('error')}")
            return
            
        g_x_str = result["g_x_str_latex"]
        print(f"Hàm xấp xỉ: g(x) = {g_x_str}")

        plt.figure(figsize=(10, 6))
        plt.plot(x_data, y_data, 'o', color='blue', markersize=8, label='Data Points')

        x_sym = symbols('x')
        g_x_lambda = lambdify(x_sym, sympify(g_x_str.replace('\\cdot', '*')), 'numpy')

        x_fit = np.linspace(min(x_data), max(x_data), 100)
        y_fit = g_x_lambda(x_fit)
        
        plt.plot(x_fit, y_fit, 'r-', label=f'Hàm xấp xỉ g(x)')
        plt.title('Kiểm tra Bình phương tối thiểu (Đường thẳng)')
        plt.xlabel('Trục X'); plt.ylabel('Trục Y')
        plt.legend(); plt.grid(True, linestyle='--', alpha=0.6)
        
        output_filename = 'test_least_squares_simple.png'
        plt.savefig(output_filename)
        print(f"Đã lưu đồ thị vào file: {output_filename}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        import traceback
        traceback.print_exc()

def test_least_squares_complex_plot():
    """
    Kiểm tra LSQ với dữ liệu phi tuyến, nhiều điểm và có nhiễu.
    """
    print("\n--- Bắt đầu kiểm tra Bình phương tối thiểu (Phức tạp) ---")
    
    np.random.seed(42) # Để kết quả nhiễu có thể lặp lại
    N_POINTS = 50
    
    # 1. Tạo dữ liệu gốc
    x_data = np.linspace(0, 10, N_POINTS)
    # Hàm gốc: f(x) = 0.1x^2 + 2sin(x) + 5
    y_true = 0.1 * (x_data**2) + 2 * np.sin(x_data) + 5
    # Thêm nhiễu
    noise = np.random.normal(0, 0.5, size=x_data.shape)
    y_data = y_true + noise
    
    # 2. Chọn hàm cơ sở
    # Thử mô hình g(x) = a1*1 + a2*x + a3*x^2 + a4*sin(x)
    basis_funcs_str = ['1', 'x', 'x**2', 'sin(x)']
    
    print(f"Dữ liệu: {N_POINTS} điểm, dựa trên 0.1x^2 + 2sin(x) + 5 + nhiễu")
    print(f"Hàm cơ sở xấp xỉ: {basis_funcs_str}")

    try:
        # 3. Gọi hàm tính toán
        result = least_squares_approximation(x_data.tolist(), y_data.tolist(), basis_funcs_str)
        if result["status"] != "success":
            print(f"Lỗi: {result.get('error')}")
            return
            
        a = result["coefficients"]
        g_x_str = result["g_x_str_latex"]
        print(f"Hàm xấp xỉ: g(x) = {g_x_str}")
        print(f"Các hệ số: a = {[float(f'{c:.4f}') for c in a]}")
        print(f"Sai số TB phương: {result['error_metrics']['std_error']:.4f}")

        # 4. Chuẩn bị vẽ đồ thị
        plt.figure(figsize=(10, 6))
        # Vẽ dữ liệu nhiễu
        plt.plot(x_data, y_data, 'o', color='blue', markersize=4, alpha=0.7, label='Data Points (w/ Noise)')
        # Vẽ hàm gốc
        plt.plot(x_data, y_true, '--', color='gray', linewidth=2, label='Hàm gốc f(x)')

        # 5. Vẽ hàm xấp xỉ
        x_sym = symbols('x')
        g_x_lambda = lambdify(x_sym, sympify(g_x_str.replace('\\cdot', '*')), 'numpy')

        x_fit = np.linspace(min(x_data), max(x_data), 200)
        y_fit = g_x_lambda(x_fit)
        
        plt.plot(x_fit, y_fit, 'r-', linewidth=2, label=f'Hàm xấp xỉ g(x)')
        plt.title('Kiểm tra Bình phương tối thiểu (Phức tạp)')
        plt.xlabel('Trục X'); plt.ylabel('Trục Y')
        plt.legend(); plt.grid(True, linestyle='--', alpha=0.6)
        
        output_filename = 'test_least_squares_complex.png'
        plt.savefig(output_filename)
        print(f"Đã lưu đồ thị vào file: {output_filename}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        import traceback
        traceback.print_exc()


def test_least_squares_trigonometric_plot():
    """
    Kiểm tra LSQ với dữ liệu từ spline và bộ hàm cơ sở lượng giác.
    """
    print("\n--- Bắt đầu kiểm tra Bình phương tối thiểu (Lượng giác) ---")
    
    # 1. Dữ liệu (từ yêu cầu của bạn, giống hệt dữ liệu spline)
    x_data = [0.3, 0.7, 1.2, 1.5, 1.8, 2.2, 2.6, 3.0]
    y_data = [1.2, 2.7, 3.0, 2.3, 3.2, 1.0, 0.8, 7.0]
    
    # 2. Hàm cơ sở (từ yêu cầu của bạn)
    basis_funcs_str = ['1', 'sin(x)', 'cos(x)', 'sin(2*x)', 'cos(2*x)', 'sin(3*x)', 'cos(3*x)']
    
    print(f"Dữ liệu X: {x_data}")
    print(f"Dữ liệu Y: {y_data}")
    print(f"Hàm cơ sở: {basis_funcs_str}")

    try:
        # 3. Gọi hàm tính toán
        result = least_squares_approximation(x_data, y_data, basis_funcs_str)
        if result["status"] != "success":
            print(f"Lỗi: {result.get('error')}")
            return
            
        a = result["coefficients"]
        g_x_str = result["g_x_str_latex"]
        print(f"Hàm xấp xỉ: g(x) = {g_x_str}")
        print(f"Các hệ số: a = {[float(f'{c:.4f}') for c in a]}")
        print(f"Sai số TB phương: {result['error_metrics']['std_error']:.4f}")

        # 4. Chuẩn bị vẽ đồ thị
        plt.figure(figsize=(10, 6))
        # Vẽ dữ liệu điểm
        plt.plot(x_data, y_data, 'o', color='blue', markersize=8, label='Data Points')

        # 5. Vẽ hàm xấp xỉ
        x_sym = symbols('x')
        # Thay thế \cdot bằng * để sympify hiểu
        g_x_str_sympy = g_x_str.replace('\\cdot', '*')
        
        # Thêm thư viện numpy vào cho lambdify
        g_x_lambda = lambdify(x_sym, sympify(g_x_str_sympy), 'numpy')

        x_fit = np.linspace(min(x_data), max(x_data), 200)
        y_fit = g_x_lambda(x_fit)
        
        plt.plot(x_fit, y_fit, 'r-', linewidth=2, label=f'Hàm xấp xỉ g(x)')
        plt.title('Kiểm tra Bình phương tối thiểu (Hàm lượng giác)')
        plt.xlabel('Trục X'); plt.ylabel('Trục Y')
        plt.legend(); plt.grid(True, linestyle='--', alpha=0.6)
        
        output_filename = 'test_least_squares_trig.png'
        plt.savefig(output_filename)
        print(f"Đã lưu đồ thị vào file: {output_filename}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Chạy tất cả các bài test
    test_linear_spline_plot()
    test_quadratic_spline_plot()
    test_cubic_spline_plot()
    test_least_squares_simple_plot()
    test_least_squares_complex_plot()
    test_least_squares_trigonometric_plot() # Thêm test mới
    
    print("\nĐã chạy tất cả các kiểm tra.")