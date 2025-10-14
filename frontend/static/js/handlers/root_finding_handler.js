// frontend/static/js/handlers/root_finding_handler.js
import { solveNonlinearEquation } from '../api.js';
import { renderRootFindingSolution, showLoading, hideLoading, showError } from '../ui.js';

/**
 * Chuyển đổi chuỗi LaTeX thành chuỗi biểu thức Python mà SymPy có thể hiểu.
 * @param {string} latex - Chuỗi LaTeX đầu vào.
 * @returns {string} - Chuỗi biểu thức Python.
 */
function latexToPython(latex) {
    if (!latex) return "";
    let pyExpr = latex.trim();

    // Các thay thế ưu tiên cao
    pyExpr = pyExpr.replace(/\\sqrt\[(.*?)\]\{(.*?)\}/g, '($2)**(1/($1))'); // Căn bậc n
    pyExpr = pyExpr.replace(/\\sqrt\{(.*?)\}/g, 'sqrt($1)'); // Căn bậc 2
    pyExpr = pyExpr.replace(/\\frac\{(.*?)\}\{(.*?)\}/g, '($1)/($2)'); // Phân số
    pyExpr = pyExpr.replace(/\\log_\{(.*?)\}\{(.*?)\}/g, 'log($2, $1)'); // Log cơ số a
    pyExpr = pyExpr.replace(/([a-zA-Z])_\{?(\d+)\}?/g, '$1$2'); // Biến có chỉ số, ví dụ x_1 -> x1

    // Các hàm chuẩn
    pyExpr = pyExpr.replace(/\\(sin|cos|tan|asin|acos|atan|ln|log|exp|abs|pi)/g, '$1');

    // Các toán tử và ký hiệu
    pyExpr = pyExpr.replace(/\^/g, '**');      // Lũy thừa
    pyExpr = pyExpr.replace(/\\cdot/g, '*');    // Phép nhân
    pyExpr = pyExpr.replace(/\{/g, '(');      // Mở ngoặc
    pyExpr = pyExpr.replace(/\}/g, ')');      // Đóng ngoặc
    
    // Xóa các khoảng trắng thừa
    pyExpr = pyExpr.replace(/\s+/g, ' ').trim();

    return pyExpr;
}

/**
 * Hiển thị (render) biểu thức LaTeX từ một ô input vào một khu vực xem trước.
 * @param {HTMLInputElement} inputElement - Ô input chứa mã LaTeX.
 * @param {HTMLElement} previewElement - Vùng div để hiển thị kết quả render.
 */
function renderLatex(inputElement, previewElement) {
    if (!inputElement || !previewElement) return;
    const latex = inputElement.value.trim();

    // Luôn đặt lại style về mặc định trước khi render
    previewElement.innerHTML = '';
    previewElement.className = 'mt-2 p-3 bg-gray-50 rounded-md min-h-[50px] flex items-center justify-center text-lg';

    if (latex === "") {
        previewElement.textContent = 'Xem trước biểu thức...';
        previewElement.classList.add('text-gray-400');
        return;
    }
    
    previewElement.classList.remove('text-gray-400');

    try {
        // Nếu render thành công, style mặc định đã được áp dụng
        katex.render(latex, previewElement, {
            throwOnError: true,
            displayMode: true
        });
    } catch (error) {
        // Nếu lỗi, ghi đè style mặc định bằng style báo lỗi
        previewElement.textContent = `Lỗi cú pháp LaTeX: ${error.message}`;
        previewElement.className = 'text-red-500 text-sm p-3 bg-red-50 rounded-md min-h-[50px] flex items-center justify-center';
    }
}

/**
 * Xử lý việc hiển thị/ẩn các tùy chọn nâng cao và các ô input dựa trên phương pháp được chọn.
 */
function updateMethodUI() {
    const method = document.getElementById('nonlinear-method-select').value;
    const fGroup = document.getElementById('f-expression-group');
    const phiGroup = document.getElementById('phi-expression-group');
    const advancedGroup = document.getElementById('advanced-stop-condition-group');
    const x0Group = document.getElementById('x0-group');
    
    // Ẩn tất cả các nhóm tùy chọn đặc biệt trước
    fGroup.style.display = 'none';
    phiGroup.style.display = 'none';
    advancedGroup.style.display = 'none';
    x0Group.style.display = 'none';

    if (method === 'bisection') {
        fGroup.style.display = 'block';
    } else if (method === 'secant') {
        fGroup.style.display = 'block';
        advancedGroup.style.display = 'block';
        katex.render('\\frac{|f(x_n)|}{m_1}', document.getElementById('adv-stop-label-1'));
        katex.render('\\frac{M_1 - m_1}{m_1} |x_n - x_{n-1}|', document.getElementById('adv-stop-label-2'));
    } else if (method === 'newton') {
        fGroup.style.display = 'block';
        advancedGroup.style.display = 'block';
        x0Group.style.display = 'block';
        katex.render('\\frac{|f(x_{n+1})|}{m_1}', document.getElementById('adv-stop-label-1'));
        katex.render('\\frac{M_2}{2m_1} |x_{n+1} - x_n|^2', document.getElementById('adv-stop-label-2'));
    } else if (method === 'simple_iteration') {
        phiGroup.style.display = 'block';
        x0Group.style.display = 'block';
    }
}

export function setupRootFindingHandlers() {
    const calculateBtn = document.getElementById('calculate-nonlinear-btn');
    const fInput = document.getElementById('f-expression-input');
    const fPreview = document.getElementById('f-latex-preview');
    const phiInput = document.getElementById('phi-expression-input');
    const phiPreview = document.getElementById('phi-latex-preview');
    const methodSelect = document.getElementById('nonlinear-method-select');

    if (methodSelect) {
        methodSelect.addEventListener('change', updateMethodUI);
    }

    if (fInput) {
        fInput.addEventListener('input', () => renderLatex(fInput, fPreview));
        renderLatex(fInput, fPreview); 
    }
    
    if (phiInput) {
        phiInput.addEventListener('input', () => renderLatex(phiInput, phiPreview));
        renderLatex(phiInput, phiPreview);
    }

    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleCalculation);
    }
    
    // Khởi tạo trạng thái giao diện khi tải trang
    updateMethodUI();
}

async function handleCalculation() {
    const method = document.getElementById('nonlinear-method-select').value;
    const a = document.getElementById('interval-a-input').value;
    const b = document.getElementById('interval-b-input').value;
    const stop_mode = document.getElementById('stop-mode-select').value;
    const stop_value = document.getElementById('stop-value-input').value;
    const x0 = document.getElementById('x0-input').value;

    if (!a.trim() || !b.trim() || !stop_value.trim()) {
        showError('Vui lòng nhập đầy đủ khoảng [a, b] và giá trị điều kiện dừng.');
        return;
    }

    const payload = {
        method, a, b, stop_mode, stop_value, x0
    };

    if (method === 'simple_iteration') {
        const phiLatex = document.getElementById('phi-expression-input').value;
        if (!phiLatex.trim()) {
            showError('Vui lòng nhập hàm lặp φ(x).');
            return;
        }
        if (!x0.trim()) {
            showError('Vui lòng nhập điểm bắt đầu x₀.');
            return;
        }
        payload.phi_expression = latexToPython(phiLatex);
    } else {
        const latexExpression = document.getElementById('f-expression-input').value;
        if (!latexExpression.trim()) {
            showError('Vui lòng nhập biểu thức f(x).');
            return;
        }
        payload.expression = latexToPython(latexExpression);
    }
    
    if (method === 'secant' || method === 'newton') {
        payload.adv_stop_condition = document.querySelector('input[name="advanced-stop-option"]:checked').value;
    }
     if (method === 'newton' && !x0.trim()){
        showError('Vui lòng nhập điểm bắt đầu x₀.');
        return;
    }


    showLoading();
    try {
        const data = await solveNonlinearEquation(payload);
        renderRootFindingSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}