// frontend/static/js/handlers/iterative_methods_handler.js
import { solveIterativeLinearSystem } from '../api.js';
import { renderIterativeSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupIterativeMethodsHandlers() {
    const calculateJacobiBtn = document.getElementById('calculate-jacobi-btn');
    if (calculateJacobiBtn) {
        calculateJacobiBtn.addEventListener('click', handleJacobiCalculation);
    }
    const calculateGSBtn = document.getElementById('calculate-gs-btn');
    if (calculateGSBtn) {
        calculateGSBtn.addEventListener('click', handleGaussSeidelCalculation);
    }
}

async function handleJacobiCalculation() {
    const matrixA = document.getElementById('matrix-a-input-iter').value;
    const matrixB = document.getElementById('matrix-b-input-iter').value;
    const x0 = document.getElementById('x0-input-iter').value;
    const tolerance = document.getElementById('iter-tolerance').value;
    const maxIter = document.getElementById('iter-max-iter').value;
    
    if (!matrixA.trim() || !matrixB.trim() || !x0.trim()) {
        showError('Vui lòng nhập đầy đủ các ma trận A, b và vector lặp ban đầu X₀.');
        return;
    }

    showLoading();
    
    try {
        const data = await solveIterativeLinearSystem('jacobi', matrixA, matrixB, x0, tolerance, maxIter);
        renderIterativeSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function handleGaussSeidelCalculation() {
    // Xử lý sự kiện cho nút Gauss-Seidel.
    const matrixA = document.getElementById('matrix-a-input-iter').value;
    const matrixB = document.getElementById('matrix-b-input-iter').value;
    const x0 = document.getElementById('x0-input-iter').value;
    const tolerance = document.getElementById('iter-tolerance').value;
    const maxIter = document.getElementById('iter-max-iter').value;
    
    if (!matrixA.trim() || !matrixB.trim() || !x0.trim()) {
        showError('Vui lòng nhập đầy đủ các ma trận A, b và vector lặp ban đầu X₀.');
        return;
    }

    showLoading();
    
    try {
        const data = await solveIterativeLinearSystem('gauss-seidel', matrixA, matrixB, x0, tolerance, maxIter);
        renderIterativeSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}
