// frontend/static/js/handlers/interpolation_methods_handler.js
import { getChebyshevNodes } from '../api.js';
import { renderInterpolationSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupInterpolationHandlers() {
    const calculateBtn = document.getElementById('calculate-optimal-nodes-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleChebyshevCalculation);
    }
    // Thêm các handlers khác cho Lagrange, Newton... ở đây khi cần
}

async function handleChebyshevCalculation() {
    const n = document.getElementById('optimal-n-input').value;
    const a = document.getElementById('optimal-a-input').value;
    const b = document.getElementById('optimal-b-input').value;

    if (!n.trim() || !a.trim() || !b.trim()) {
        showError('Vui lòng nhập đầy đủ số mốc (n) và khoảng [a, b].');
        return;
    }

    showLoading();
    try {
        const data = await getChebyshevNodes(a, b, n);
        // Sử dụng một hàm render chung cho các kết quả nội suy
        renderInterpolationSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}