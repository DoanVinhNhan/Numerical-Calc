import unittest
import os
import sys
import io
import pandas as pd

# --- Thêm đường dẫn dự án vào sys.path ---
# Điều này giả định test.py nằm ở thư mục gốc của dự án,
# cùng cấp với thư mục 'backend'.
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --- Kết thúc thêm đường dẫn ---

try:
    from backend.numerical_methods.interpolation.node_selection import select_interpolation_nodes
except ImportError:
    print("\nLỗi: Không thể import `select_interpolation_nodes`.")
    print("Hãy đảm bảo rằng file test.py đang ở thư mục gốc của dự án 'Numerical-Calc-...'")
    print("Và file cần test đang ở: backend/numerical_methods/interpolation/node_selection.py\n")
    sys.exit(1)

# --- SỬA LỖI: Định nghĩa đường dẫn file ở đây ---
# Định nghĩa đường dẫn file CSV như một hằng số
CSV_FILE_PATH = '20241GKtest2.csv'
# ---------------------------------------------

class TestNodeSelection(unittest.TestCase):
    """
    Các trường hợp kiểm thử cho hàm select_interpolation_nodes
    sử dụng file dữ liệu 20241GKtest2.csv.
    """

    @classmethod
    def setUpClass(cls):
        """
        Tải nội dung file CSV vào bộ nhớ một lần trước khi chạy các test case.
        """
        # --- SỬA LỖI: Sử dụng hằng số đã định nghĩa ---
        cls.csv_file_path = CSV_FILE_PATH 
        if not os.path.exists(cls.csv_file_path):
            raise FileNotFoundError(
                f"Không tìm thấy file {cls.csv_file_path}. "
                "Hãy đảm bảo file này nằm cùng cấp với test.py."
            )
        
        with open(cls.csv_file_path, 'rb') as f:
            cls.file_content = f.read()

    def test_select_both_center(self):
        """
        Kiểm tra phương pháp 'both' (lấy lân cận hai phía).
        Chọn 4 mốc gần nhất với x_bar = 3.5.
        
        Dữ liệu gốc quanh 3.5:
        ...
        3.34, 6.5061   (dist = 0.160) - 3rd
        3.457, 6.4321 (dist = 0.043) - 1st
        --- (x_bar = 3.5) ---
        3.574, 6.3054 (dist = 0.074) - 2nd
        3.691, 6.1283 (dist = 0.191) - 4th
        3.808, 5.9039 (dist = 0.308)
        ...
        Các mốc được chọn (đã sắp xếp): [3.34, 3.457, 3.574, 3.691]
        """
        print("\nĐang kiểm tra: [both], x_bar=3.5, num_nodes=4")
        stream = io.BytesIO(self.file_content)
        result = select_interpolation_nodes(stream, x_bar=3.5, num_nodes=4, method='both')
        
        expected_x = [3.34, 3.457, 3.574, 3.691]
        expected_y = [6.5061, 6.4321, 6.3054, 6.1283]
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['num_nodes_found'], 4)
        # Sử dụng assertAlmostEqual cho so sánh số thực
        for res_x, exp_x in zip(result['selected_x'], expected_x):
            self.assertAlmostEqual(res_x, exp_x)
        for res_y, exp_y in zip(result['selected_y'], expected_y):
            self.assertAlmostEqual(res_y, exp_y)

    def test_select_left(self):
        """
        Kiểm tra phương pháp 'left' (lấy mốc bên trái).
        Chọn 4 mốc bên trái gần nhất với x_bar = 3.5 (tức là x <= 3.5).
        
        Dữ liệu gốc:
        ...
        3.106, 6.4899
        3.223, 6.5257
        3.34, 6.5061
        3.457, 6.4321
        --- (x_bar = 3.5) ---
        ...
        Các mốc được chọn (đã sắp xếp): [3.106, 3.223, 3.34, 3.457]
        """
        print("\nĐang kiểm tra: [left], x_bar=3.5, num_nodes=4")
        stream = io.BytesIO(self.file_content)
        result = select_interpolation_nodes(stream, x_bar=3.5, num_nodes=4, method='left')
        
        expected_x = [3.106, 3.223, 3.34, 3.457]
        expected_y = [6.4899, 6.5257, 6.5061, 6.4321]
        
        self.assertEqual(result['status'], 'success')
        for res_x, exp_x in zip(result['selected_x'], expected_x):
            self.assertAlmostEqual(res_x, exp_x)
        for res_y, exp_y in zip(result['selected_y'], expected_y):
            self.assertAlmostEqual(res_y, exp_y)

    def test_select_right(self):
        """
        Kiểm tra phương pháp 'right' (lấy mốc bên phải).
        Chọn 4 mốc bên phải gần nhất với x_bar = 3.5 (tức là x >= 3.5).
        
        Dữ liệu gốc:
        ...
        --- (x_bar = 3.5) ---
        3.574, 6.3054
        3.691, 6.1283
        3.808, 5.9039
        3.925, 5.6358
        ...
        Các mốc được chọn (đã sắp xếp): [3.574, 3.691, 3.808, 3.925]
        """
        print("\nĐang kiểm tra: [right], x_bar=3.5, num_nodes=4")
        stream = io.BytesIO(self.file_content)
        result = select_interpolation_nodes(stream, x_bar=3.5, num_nodes=4, method='right')
        
        expected_x = [3.574, 3.691, 3.808, 3.925]
        expected_y = [6.3054, 6.1283, 5.9039, 5.6358]
        
        self.assertEqual(result['status'], 'success')
        for res_x, exp_x in zip(result['selected_x'], expected_x):
            self.assertAlmostEqual(res_x, exp_x)
        for res_y, exp_y in zip(result['selected_y'], expected_y):
            self.assertAlmostEqual(res_y, exp_y)

    def test_error_too_many_nodes(self):
        """
        Kiểm tra lỗi khi yêu cầu số mốc nhiều hơn số mốc có trong file.
        """
        print("\nĐang kiểm tra: Lỗi yêu cầu quá nhiều mốc")
        stream = io.BytesIO(self.file_content)
        with self.assertRaises(ValueError) as context:
            select_interpolation_nodes(stream, x_bar=3.5, num_nodes=200, method='both')
        
        self.assertIn("lớn hơn số điểm dữ liệu", str(context.exception))

    def test_error_not_enough_nodes_left(self):
        """
        Kiểm tra lỗi khi không có đủ mốc bên trái x_bar.
        """
        print("\nĐang kiểm tra: Lỗi không đủ mốc bên trái")
        stream = io.BytesIO(self.file_content)
        # Điểm x nhỏ nhất trong file là 1.0
        with self.assertRaises(ValueError) as context:
            select_interpolation_nodes(stream, x_bar=0.5, num_nodes=4, method='left')
            
        self.assertIn("Không tìm thấy đủ", str(context.exception))
        self.assertIn("bên trái", str(context.exception))

    def test_error_not_enough_nodes_right(self):
        """
        Kiểm tra lỗi khi không có đủ mốc bên phải x_bar.
        """
        print("\nĐang kiểm tra: Lỗi không đủ mốc bên phải")
        stream = io.BytesIO(self.file_content)
        # Điểm x lớn nhất trong file là 13.285
        with self.assertRaises(ValueError) as context:
            select_interpolation_nodes(stream, x_bar=14.0, num_nodes=4, method='right')
            
        self.assertIn("Không tìm thấy đủ", str(context.exception))
        self.assertIn("bên phải", str(context.exception))

    def test_error_bad_csv_format(self):
        """
        Kiểm tra lỗi khi file CSV có định dạng hoàn toàn sai.
        """
        print("\nĐang kiểm tra: Lỗi file CSV không hợp lệ")
        bad_content = b"day la file text\nkhong phai la file csv\na,b,c"
        bad_stream = io.BytesIO(bad_content)
        with self.assertRaises(ValueError) as context:
            select_interpolation_nodes(bad_stream, x_bar=1.0, num_nodes=2, method='both')
            
        self.assertIn("không chứa dữ liệu số", str(context.exception))

    def test_error_empty_file(self):
        """
        Kiểm tra lỗi khi file CSV rỗng.
        """
        print("\nĐang kiểm tra: Lỗi file rỗng")
        empty_content = b""
        empty_stream = io.BytesIO(empty_content)
        with self.assertRaises(ValueError) as context:
            select_interpolation_nodes(empty_stream, x_bar=1.0, num_nodes=2, method='both')
            
        self.assertIn("không chứa dữ liệu số", str(context.exception))

if __name__ == '__main__':
    print(f"--- Bắt đầu kiểm tra cho 'node_selection.py' ---")
    
    # --- SỬA LỖI Ở ĐÂY ---
    # In hằng số toàn cục thay vì thuộc tính lớp chưa được khởi tạo
    print(f"Sử dụng file dữ liệu: '{CSV_FILE_PATH}'")
    # ---------------------
    
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestNodeSelection))
    
    # Chạy test với verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)