// frontend/static/js/handlers/nonlinear_systems_handler.js
import { solveNonlinearSystem } from '../api.js';
import { renderNonlinearSystemSolution, showLoading, hideLoading, showError } from '../ui.js';

/**
 * Chuyển đổi chuỗi LaTeX thành chuỗi biểu thức Python mà SymPy có thể hiểu.
 * Hỗ trợ các biến có chỉ số như x_1, x_2.
 */
function latexToPython(latex) {
    if (!latex) return "";
    let pyExpr = latex.trim();

    // Thay thế các biến có chỉ số (ví dụ: x_{1}, x_2) thành (x1, x2)
    pyExpr = pyExpr.replace(/x_\{?(\d+)\}?/g, 'x$1'); 
    
    // Các thay thế khác tương tự như root_finding_handler
    pyExpr = pyExpr.replace(/\\sqrt\[(.*?)\]\{(.*?)\}/g, '($2)**(1/($1))');
    pyExpr = pyExpr.replace(/\\sqrt\{(.*?)\}/g, 'sqrt($1)');
    pyExpr = pyExpr.replace(/\\frac\{(.*?)\}\{(.*?)\}/g, '($1)/($2)');
    pyExpr = pyExpr.replace(/\\log_\{(.*?)\}\{(.*?)\}/g, 'log($2, $1)');
    pyExpr = pyExpr.replace(/\\(sin|cos|tan|asin|acos|atan|ln|log|exp|abs|pi)/g, '$1');
    pyExpr = pyExpr.replace(/\^/g, '**');
    pyExpr = pyExpr.replace(/\\cdot/g, '*');
    pyExpr = pyExpr.replace(/\{/g, '(');
    pyExpr = pyExpr.replace(/\}/g, ')');
    
    return pyExpr.replace(/\s+/g, ' ').trim();
}

/**
 * Render preview cho hệ phương trình.
 */
function renderSystemLatex(inputElement, previewElement) {
    if (!inputElement || !previewElement) return;
    
    const latexLines = inputElement.value.trim().split('\n');
    previewElement.innerHTML = '';
    previewElement.className = 'mt-2 p-3 bg-gray-50 rounded-md min-h-[80px] flex flex-col items-center justify-center text-lg space-y-2';

    if (latexLines.length === 0 || latexLines[0].trim() === "") {
        previewElement.textContent = 'Xem trước hệ phương trình...';
        previewElement.classList.add('text-gray-400');
        return;
    }
    
    previewElement.classList.remove('text-gray-400');
    
    latexLines.forEach(line => {
        const lineDiv = document.createElement('div');
        try {
            katex.render(line.trim(), lineDiv, {
                throwOnError: true,
                displayMode: false
            });
            previewElement.appendChild(lineDiv);
        } catch (error) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'text-red-500 text-sm';
            errorDiv.textContent = `Lỗi: ${error.message}`;
            previewElement.appendChild(errorDiv);
        }
    });
}


export function setupNonlinearSystemsHandlers() {
    const calculateBtn = document.getElementById('calculate-ns-btn');
    const expressionsInput = document.getElementById('ns-expressions-input');
    const previewDiv = document.getElementById('ns-latex-preview');
    
    katex.render("||X_k - X_{k-1}||_\\infty", document.getElementById('ns-norm-inf-katex'));
    katex.render("||X_k - X_{k-1}||_1", document.getElementById('ns-norm-1-katex'));
    
    if (expressionsInput) {
        expressionsInput.addEventListener('input', () => renderSystemLatex(expressionsInput, previewDiv));
        renderSystemLatex(expressionsInput, previewDiv); // Render lần đầu
    }

    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleCalculation);
    }
}

async function handleCalculation() {
    const method = document.getElementById('ns-method-select').value;
    const expressionsLatex = document.getElementById('ns-expressions-input').value.trim().split('\n');
    const x0 = document.getElementById('ns-x0-input').value.trim().split('\n');
    const stop_option = document.getElementById('ns-stop-option-select').value;
    const stop_value = document.getElementById('ns-stop-value-input').value;
    const norm_choice = document.querySelector('input[name="ns-norm-option"]:checked').value;
    
    if (expressionsLatex.some(e => e.trim() === '') || x0.some(e => e.trim() === '')) {
        showError('Vui lòng nhập đầy đủ các phương trình và giá trị ban đầu.');
        return;
    }
    
    const expressions = expressionsLatex.map(latexToPython);
    
    const payload = {
        method,
        expressions,
        x0,
        stop_option,
        stop_value,
        norm_choice
    };
    
    showLoading();
    try {
        const data = await solveNonlinearSystem(payload);
        renderNonlinearSystemSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}