// frontend/static/js/handlers/horner_handler.js
import { calculateSyntheticDivision, calculateAllDerivatives, calculateReverseHorner, calculateWFunction } from '../api.js'; // Thêm calculateWFunction
import { renderAllDerivativesSolution, renderHornerSolution, renderReverseHornerSolution, renderWFunctionSolution, showLoading, hideLoading, showError } from '../ui.js'; // Thêm renderWFunctionSolution

export function setuphornerHandlers() {
    const calculateBtn = document.getElementById('calculate-synthetic-division-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleSyntheticDivision);
    }
    const calculateAllDerivativesBtn = document.getElementById('calculate-all-derivatives-btn');
    if (calculateAllDerivativesBtn) {
        calculateAllDerivativesBtn.addEventListener('click', handleAllDerivatives);
    }
    const calculateReverseBtn = document.getElementById('calculate-reverse-horner-btn');
    if (calculateReverseBtn) {
        calculateReverseBtn.addEventListener('click', handleReverseHorner);
    }
    const calculateWBtn = document.getElementById('calculate-w-function-btn');
    if (calculateWBtn) {
        calculateWBtn.addEventListener('click', handleWFunction);
    }
}

async function handleSyntheticDivision() {
    const coeffs = document.getElementById('horner-coeffs-input').value;
    const root = document.getElementById('horner-root-input').value;

    if (!coeffs.trim() || !root.trim()) {
        showError('Vui lòng nhập đầy đủ hệ số đa thức và giá trị c.');
        return;
    }

    showLoading();
    try {
        const data = await calculateSyntheticDivision(coeffs, root);
        renderHornerSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}
async function handleAllDerivatives() {
    const coeffs = document.getElementById('all-derivatives-coeffs-input').value;
    const root = document.getElementById('all-derivatives-root-input').value;
    const order = document.getElementById('all-derivatives-order-input').value;

    if (!coeffs.trim() || !root.trim()) {
        showError('Vui lòng nhập đầy đủ hệ số đa thức và giá trị c.');
        return;
    }

    showLoading();
    try {
        const data = await calculateAllDerivatives(coeffs, root, order);
        renderAllDerivativesSolution(document.getElementById('results-area'), data); // Gọi hàm render mới
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function handleReverseHorner() {
    const coeffs = document.getElementById('reverse-horner-coeffs-input').value;
    const root = document.getElementById('reverse-horner-root-input').value;

    if (!coeffs.trim() || !root.trim()) {
        showError('Vui lòng nhập đầy đủ hệ số đa thức và giá trị c.');
        return;
    }

    showLoading();
    try {
        const data = await calculateReverseHorner(coeffs, root);
        renderReverseHornerSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function handleWFunction() {
    const roots = document.getElementById('w-function-roots-input').value;

    if (!roots.trim()) {
        showError('Vui lòng nhập các nghiệm x_i.');
        return;
    }

    showLoading();
    try {
        const data = await calculateWFunction(roots);
        renderWFunctionSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}