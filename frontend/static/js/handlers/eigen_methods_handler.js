// frontend/static/js/handlers/eigen_methods_handler.js
import { calculateEigen } from '../api.js';
import { renderEigenSolution, renderSvdSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupEigenMethodsHandlers() {
    // === Logic chuyển đổi Tab ===
    const eigenTabs = document.querySelectorAll('.eigen-tab');
    eigenTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabTarget = tab.dataset.tab;
            
            eigenTabs.forEach(t => {
                t.classList.remove('text-blue-600', 'border-blue-500');
                t.classList.add('text-gray-500', 'border-transparent');
            });
            tab.classList.add('text-blue-600', 'border-blue-500');

            document.querySelectorAll('.eigen-tab-content').forEach(content => {
                content.classList.add('hidden');
            });

            const activeContent = document.getElementById(`eigen-${tabTarget}-content`);
            if (activeContent) {
                activeContent.classList.remove('hidden');
            }
        });
    });

    // === Trình xử lý sự kiện cho Danilevsky ===
    const danilevskyBtn = document.getElementById('calculate-danilevsky-btn');
    if (danilevskyBtn) {
        danilevskyBtn.addEventListener('click', () => handleEigenCalculation('danilevsky'));
    }

    // === Trình xử lý sự kiện cho Power Method (Trị riêng trội) ===
    const powerSingleBtn = document.getElementById('calculate-power-method-single-btn');
    if(powerSingleBtn) {
        powerSingleBtn.addEventListener('click', () => handleEigenCalculation('power-single'));
    }

    // === Trình xử lý sự kiện cho Power Method (Xuống thang) ===
    const powerDeflationBtn = document.getElementById('calculate-power-method-deflation-btn');
    if (powerDeflationBtn) {
        powerDeflationBtn.addEventListener('click', () => handleEigenCalculation('power-deflation'));
    }

    // === Trình xử lý sự kiện cho SVD ===
    const calculateSvdBtn = document.getElementById('calculate-svd-btn');
    if (calculateSvdBtn) {
        calculateSvdBtn.addEventListener('click', handleSvdCalculation);
    }

    const svdMethodSelect = document.getElementById('svd-method-select');
    if (svdMethodSelect) {
        svdMethodSelect.addEventListener('change', (e) => {
            const powerOptions = document.getElementById('svd-power-options');
            if (powerOptions) {
                powerOptions.style.display = (e.target.value === 'power') ? 'block' : 'none';
            }
        });
    }
}

/**
 * Hàm chung để xử lý các yêu cầu tính toán trị riêng/vector riêng.
 * @param {string} method - Tên phương pháp (ví dụ: 'danilevsky', 'power-single').
 */
async function handleEigenCalculation(method) {
    let payload = {};
    const resultsArea = document.getElementById('results-area');

    showLoading();

    try {
        if (method === 'danilevsky') {
            const matrixA = document.getElementById('matrix-a-input-danilevsky').value;
            if (!matrixA || !matrixA.trim()) {
                showError('Vui lòng nhập ma trận A.'); return;
            }
            payload = { matrix_a: matrixA };
        } else if (method === 'power-single') {
            const matrixA = document.getElementById('matrix-a-input-power-single').value;
            if (!matrixA || !matrixA.trim()) {
                showError('Vui lòng nhập ma trận A.'); return;
            }
            payload = { 
                matrix_a: matrixA, 
                tolerance: document.getElementById('power-single-tolerance').value, 
                max_iter: document.getElementById('power-single-max-iter').value, 
                x0: document.getElementById('power-x0-input').value 
            };
        } else if (method === 'power-deflation') {
            const matrixA = document.getElementById('matrix-a-input-power-deflation').value;
            if (!matrixA || !matrixA.trim()) {
                showError('Vui lòng nhập ma trận A.'); return;
            }
            payload = { 
                matrix_a: matrixA, 
                num_values: document.getElementById('power-deflation-num-eigen').value, 
                tolerance: document.getElementById('power-deflation-tolerance').value, 
                max_iter: document.getElementById('power-deflation-max-iter').value, 
                x0: document.getElementById('power-x0-input-deflation').value
            };
        }

        const data = await calculateEigen(method, payload);
        renderEigenSolution(resultsArea, data);

    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Hàm xử lý yêu cầu tính toán SVD.
 */
async function handleSvdCalculation() {
    const matrixA = document.getElementById('matrix-a-input-svd').value;
    const method = document.getElementById('svd-method-select').value;
    const numSingular = document.getElementById('svd-num-singular').value;
    const yInit = document.getElementById('svd-init-matrix-input').value;

    if (!matrixA.trim()) {
        showError('Vui lòng nhập ma trận A.');
        return;
    }

    const payload = {
        matrix_a: matrixA,
        method: method,
        num_singular: numSingular,
        y_init: yInit
    };

    showLoading();
    try {
        // Lưu ý: route SVD được đặt trong /eigen/svd để nhất quán
        const data = await calculateEigen('svd', payload);
        renderSvdSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}