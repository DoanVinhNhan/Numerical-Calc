# Numerical Calculator - Máy Tính Giải Tích Số

Ứng dụng web được xây dựng để thực hiện các phương pháp tính toán của môn **Giải tích số / Phương pháp số** (MI3041/MI3042) tại Khoa Toán - Tin, Đại học Bách Khoa Hà Nội.

---

## Tính năng 🧮

Ứng dụng cung cấp giao diện trực quan để thực hiện và hiển thị kết quả chi tiết từng bước cho các phương pháp sau:

### 1. Đại số tuyến tính

* **Giải hệ phương trình:**
    * Phương pháp trực tiếp: Khử Gauss, Gauss-Jordan, Phân rã LU, Phân rã Cholesky.
    * Phương pháp lặp: Jacobi, Gauss-Seidel, Lặp đơn (X = BX + d).
* **Tính ma trận nghịch đảo:**
    * Phương pháp trực tiếp: Gauss-Jordan, Phân rã LU, Phân rã Cholesky, Viền quanh.
    * Phương pháp lặp: Jacobi, Gauss-Seidel, Lặp tựa Newton.
* **Phân tích giá trị riêng (Eigenvalue/Eigenvector):**
    * Phương pháp Danilevsky.
    * Phương pháp Lũy thừa (Trị riêng trội).
    * Phương pháp Lũy thừa & Xuống thang (Nhiều trị riêng).
* **Phân tích giá trị suy biến (SVD):**
    * SVD chuẩn (sử dụng thư viện).
    * SVD bằng Power Method & Deflation.
    * Ma trận xấp xỉ SVD (theo hạng k, ngưỡng, hoặc sai số).

### 2. Giải phương trình phi tuyến

* **Giải phương trình f(x) = 0:**
    * Chia đôi (Bisection).
    * Dây cung (Secant).
    * Newton (Tiếp tuyến).
    * Lặp đơn (Simple Iteration).
* **Giải phương trình đa thức:** Tự động tìm khoảng chứa nghiệm, phân ly nghiệm và tìm nghiệm thực bằng chia đôi.
* **Giải hệ phương trình phi tuyến:**
    * Phương pháp Newton.
    * Phương pháp Newton cải tiến.
    * Phương pháp Lặp đơn.

### 3. Nội suy và Xấp xỉ hàm số

* Tìm mốc nội suy tối ưu Chebyshev.
* Nội suy Lagrange.
* Tính bảng Tỷ sai phân.
* Tính bảng Sai phân (cho mốc cách đều).
* Nội suy Newton:
    * Mốc cách đều (dùng Sai phân).
    * Mốc bất kỳ (dùng Tỷ sai phân).
* Nội suy trung tâm:
    * Gauss I (số mốc lẻ).
    * *(Các phương pháp Gauss II, Stirling, Bessel có thể được bổ sung)*.

### 4. Sơ đồ Horner

* **Bảng chia Horner:** Tính P(c) và đa thức thương Q(x) khi chia P(x) cho (x-c).
* **Tính đạo hàm mọi cấp:** Tính P(c), P'(c), P''(c),... tại điểm c.
* **Đổi biến đa thức:** Chuyển P(x) thành Q(t) với t = ax + b.
* **Bảng nhân Horner:** Tính P(x) * (x-c).
* **Tính đa thức Omega:** Tính w(x) = (x - x₀)(x - x₁)...(x - x<0xE2><0x82><0x99>).

---

## Công nghệ sử dụng 💻

* **Backend:**
    * **Python:** Ngôn ngữ lập trình chính.
    * **Flask:** Web framework nhẹ để xây dựng API.
    * **NumPy:** Thư viện tính toán khoa học, xử lý ma trận hiệu quả.
    * **SymPy:** Thư viện tính toán biểu tượng (symbolic computation) để xử lý đạo hàm, biểu thức toán học.
    * **SciPy:** Thư viện bổ sung các thuật toán khoa học (ví dụ: phân rã LU, least squares).
* **Frontend:**
    * **HTML:** Cấu trúc trang web.
    * **Tailwind CSS:** Framework CSS tiện ích để tạo giao diện nhanh chóng.
    * **JavaScript (Vanilla):** Xử lý tương tác người dùng, gọi API, cập nhật giao diện.
    * **KaTeX:** Thư viện hiển thị công thức toán học dạng LaTeX.

---

## Cài đặt và Chạy ứng dụng 🚀

1.  **Clone repository:**
    ```bash
    git clone <URL_repository>
    cd numerical-calc
    ```
2.  **Tạo môi trường ảo (khuyến nghị):**
    ```bash
    python -m venv venv
    # Trên Windows:
    venv\Scripts\activate
    # Trên macOS/Linux:
    source venv/bin/activate
    ```
3.  **Cài đặt các thư viện cần thiết:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Chạy ứng dụng Flask:**
    ```bash
    python app.py
    ```
5.  Mở trình duyệt và truy cập vào địa chỉ `http://127.0.0.1:5001` (hoặc cổng được hiển thị trên terminal).

---

## Sử dụng 🖱️

* Chọn phương pháp tính toán từ menu bên trái.
* Nhập dữ liệu đầu vào (ma trận, vector, biểu thức, hệ số,...) theo định dạng yêu cầu.
    * **Ma trận/Vector:** Các số trên cùng một hàng cách nhau bằng dấu cách, các hàng cách nhau bằng dấu xuống dòng.
    * **Biểu thức (f(x), φ(x), hệ phi tuyến):** Nhập dưới dạng cú pháp LaTeX. Có ô xem trước để kiểm tra.
* Nhấn nút "Tính toán" tương ứng với phương pháp đã chọn.
* Kết quả chi tiết cùng các bước trung gian (nếu có) sẽ được hiển thị bên dưới.
* Có thể điều chỉnh **Số chữ số sau dấu phẩy** và **Ngưỡng làm tròn về 0** ở góc trên bên phải.

Chúc bạn học tốt môn Giải tích số! 👍