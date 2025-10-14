// frontend/static/js/handlers/root_finding_handler.js
import { solveNonlinearEquation } from '../api.js';
import { renderRootFindingSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupRootFindingHandlers() {
    const calculateBtn = document.getElementById('calculate-nonlinear-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleCalculation);
    }
    
    // Thêm các event listener khác cho việc thay đổi phương pháp, input... nếu cần
}

async function handleCalculation() {
    const method = document.getElementById('nonlinear-method-select').value;
    const expression = document.getElementById('f-expression-input').value;
    const a = document.getElementById('interval-a-input').value;
    const b = document.getElementById('interval-b-input').value;
    const stop_mode = document.getElementById('stop-mode-select').value;
    const stop_value = document.getElementById('stop-value-input').value;

    if (!expression.trim() || !a.trim() || !b.trim() || !stop_value.trim()) {
        showError('Vui lòng nhập đầy đủ biểu thức, khoảng [a, b] và giá trị điều kiện dừng.');
        return;
    }

    const payload = {
        method,
        expression,
        a,
        b,
        stop_mode,
        stop_value
    };

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