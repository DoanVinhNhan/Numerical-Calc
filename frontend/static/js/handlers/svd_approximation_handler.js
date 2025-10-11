// frontend/static/js/handlers/svd_approximation_handler.js
import { calculateSvdApproximation } from '../api.js';
import { renderSvdApproximationSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupSvdApproximationHandlers() {
    const methodSelect = document.getElementById('approx-method-select');
    if (methodSelect) {
        methodSelect.addEventListener('change', handleMethodChange);
    }

    const calculateBtn = document.getElementById('calculate-approximation-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleCalculation);
    }

    // Khởi tạo trạng thái ban đầu
    handleMethodChange();
}

function handleMethodChange() {
    const method = document.getElementById('approx-method-select')?.value;
    const rankKOptions = document.getElementById('rank-k-options');
    const thresholdOptions = document.getElementById('threshold-options');
    const errorBoundOptions = document.getElementById('error-bound-options');

    // Ẩn tất cả các tùy chọn
    if (rankKOptions) rankKOptions.classList.add('hidden');
    if (thresholdOptions) thresholdOptions.classList.add('hidden');
    if (errorBoundOptions) errorBoundOptions.classList.add('hidden');

    // Hiển thị tùy chọn tương ứng
    if (method === 'rank-k' && rankKOptions) {
        rankKOptions.classList.remove('hidden');
    } else if (method === 'threshold' && thresholdOptions) {
        thresholdOptions.classList.remove('hidden');
    } else if (method === 'error-bound' && errorBoundOptions) {
        errorBoundOptions.classList.remove('hidden');
    }
}

async function handleCalculation() {
    const matrixA = document.getElementById('matrix-a-input-approx').value;
    const method = document.getElementById('approx-method-select').value;
    const resultsArea = document.getElementById('results-area');

    let value;
    if (method === 'rank-k') {
        value = document.getElementById('rank-k-value').value;
    } else if (method === 'threshold') {
        value = document.getElementById('threshold-value').value;
    } else if (method === 'error-bound') {
        value = document.getElementById('error-bound-value').value;
    }

    if (!matrixA.trim()) {
        showError('Vui lòng nhập ma trận A.');
        return;
    }
    if (!value.trim()) {
        showError('Vui lòng nhập giá trị cho phương pháp xấp xỉ.');
        return;
    }

    showLoading();

    try {
        const data = await calculateSvdApproximation(matrixA, method, value);
        renderSvdApproximationSolution(resultsArea, data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}