// frontend/static/js/handlers/eigen_methods_handler.js
import { calculateSvd } from '../api.js';
import { renderSvdSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupEigenMethodsHandlers() {
    // === SVD Handlers ===
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

    // === Các handlers khác cho Danilevsky, Power Method sẽ được thêm vào đây ===
}

async function handleSvdCalculation() {
    const matrixA = document.getElementById('matrix-a-input-svd').value;
    const method = document.getElementById('svd-method-select').value;
    const numSingular = document.getElementById('svd-num-singular').value;
    const yInit = document.getElementById('svd-init-matrix-input').value;

    if (!matrixA.trim()) {
        showError('Vui lòng nhập ma trận A.');
        return;
    }

    showLoading();
    try {
        const data = await calculateSvd(matrixA, method, numSingular, yInit);
        renderSvdSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}