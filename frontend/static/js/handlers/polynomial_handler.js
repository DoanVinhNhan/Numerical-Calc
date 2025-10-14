// frontend/static/js/handlers/polynomial_handler.js
import { solvePolynomial } from '../api.js';
import { renderPolynomialSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupPolynomialHandlers() {
    const calculateBtn = document.getElementById('calculate-poly-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleCalculation);
    }
}

async function handleCalculation() {
    const coeffs = document.getElementById('poly-coeffs-input').value;
    const tolerance = document.getElementById('poly-tolerance').value;
    const maxIter = document.getElementById('poly-max-iter').value;

    if (!coeffs.trim()) {
        showError('Vui lòng nhập các hệ số của đa thức.');
        return;
    }

    showLoading();
    try {
        const data = await solvePolynomial(coeffs, tolerance, maxIter);
        renderPolynomialSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}