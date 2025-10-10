// frontend/static/js/handlers/inverse_iterative_methods_handler.js
import { calculateInverseIterative } from '../api.js';
import { renderInverseIterativeSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupInverseIterativeMethodsHandlers() {
    const calculateBtn = document.getElementById('calculate-inv-jacobi-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleJacobiInverseCalculation);
    }
}

async function handleJacobiInverseCalculation() {
    const matrixA = document.getElementById('matrix-a-input-inv-iter').value;
    const tolerance = document.getElementById('inv-iter-tolerance').value;
    const maxIter = document.getElementById('inv-iter-max-iter').value;
    const x0Method = document.getElementById('inv-iter-x0-select').value;

    if (!matrixA.trim()) {
        showError('Vui lòng nhập ma trận A.');
        return;
    }

    showLoading();
    try {
        const data = await calculateInverseIterative('jacobi', matrixA, tolerance, maxIter, x0Method);
        renderInverseIterativeSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}