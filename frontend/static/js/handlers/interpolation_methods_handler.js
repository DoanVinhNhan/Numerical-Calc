// frontend/static/js/handlers/interpolation_methods_handler.js
import { calculateFiniteDifference, getChebyshevNodes, calculateLagrangeInterpolation, calculateDividedDifference } from '../api.js';
import { renderInterpolationSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupInterpolationHandlers() {
    const calculateBtn = document.getElementById('calculate-optimal-nodes-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleChebyshevCalculation);
    }
    const calculateLagrangeBtn = document.getElementById('calculate-lagrange-btn');
    if (calculateLagrangeBtn) {
        calculateLagrangeBtn.addEventListener('click', handleLagrangeCalculation);
    }
    const calculateDividedBtn = document.getElementById('calculate-divided-difference-btn');
    if (calculateDividedBtn) {
        calculateDividedBtn.addEventListener('click', handleDividedDifferenceCalculation);
    }
    const calculateFiniteDiffBtn = document.getElementById('calculate-finite-difference-btn');
    if (calculateFiniteDiffBtn) {
        calculateFiniteDiffBtn.addEventListener('click', handleFiniteDifferenceCalculation);
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

async function handleLagrangeCalculation() {
    const xNodes = document.getElementById('lagrange-x-nodes').value;
    const yNodes = document.getElementById('lagrange-y-nodes').value;

    if (!xNodes.trim() || !yNodes.trim()) {
        showError('Vui lòng nhập đầy đủ các mốc x và giá trị y.');
        return;
    }

    showLoading();
    try {
        const data = await calculateLagrangeInterpolation(xNodes, yNodes);
        renderInterpolationSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function handleDividedDifferenceCalculation() {
    const xNodes = document.getElementById('newton-divided-x-nodes').value;
    const yNodes = document.getElementById('newton-divided-y-nodes').value;

    if (!xNodes.trim() || !yNodes.trim()) {
        showError('Vui lòng nhập đầy đủ các mốc x và giá trị y.');
        return;
    }

    showLoading();
    try {
        const data = await calculateDividedDifference(xNodes, yNodes);
        renderInterpolationSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function handleFiniteDifferenceCalculation() {
    const xNodes = document.getElementById('finite-diff-x-nodes').value;
    const yNodes = document.getElementById('finite-diff-y-nodes').value;

    if (!xNodes.trim() || !yNodes.trim()) {
        showError('Vui lòng nhập đầy đủ các mốc x và giá trị y.');
        return;
    }

    showLoading();
    try {
        const data = await calculateFiniteDifference(xNodes, yNodes);
        renderInterpolationSolution(document.getElementById('results-area'), data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}