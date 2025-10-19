// frontend/static/js/handlers/interpolation_methods_handler.js
import { calculateFiniteDifference, getChebyshevNodes, calculateLagrangeInterpolation, calculateDividedDifference, calculateNewtonInterpolation, calculateCentralInterpolation } from '../api.js';
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
    const calculateNewtonBtn = document.getElementById('calculate-newton-interpolation-btn');
    if (calculateNewtonBtn) {
        calculateNewtonBtn.addEventListener('click', handleNewtonInterpolation);
    }
    const newtonMethodSelect = document.getElementById('newton-method-select');
    if (newtonMethodSelect) {
        newtonMethodSelect.addEventListener('change', updateNewtonMethodNote);
        updateNewtonMethodNote();
    }
    const centralMethodSelect = document.getElementById('central-method-select'); // <<< THÊM LISTENER (optional for notes)
    if (centralMethodSelect) {
        centralMethodSelect.addEventListener('change', updateCentralMethodNote);
        updateCentralMethodNote(); // Initial call
    }
    const calculateCentralBtn = document.getElementById('calculate-central-interpolation-btn'); // <<< THÊM LISTENER
    if (calculateCentralBtn) {
        calculateCentralBtn.addEventListener('click', handleCentralInterpolationCalculation);
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

async function handleNewtonInterpolation() {
    const xNodes = document.getElementById('newton-x-nodes').value;
    const yNodes = document.getElementById('newton-y-nodes').value;
    const methodType = document.getElementById('newton-method-select').value; // <<< Lấy giá trị method

    if (!xNodes.trim() || !yNodes.trim()) {
        showError('Vui lòng nhập đầy đủ các mốc x và giá trị y.');
        return;
    }

    showLoading();
    try {
        // <<< Truyền methodType vào hàm API >>>
        const data = await calculateNewtonInterpolation(xNodes, yNodes, methodType);
        renderInterpolationSolution(document.getElementById('results-area'), data); // Dùng chung render
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

function updateNewtonMethodNote() {
    const select = document.getElementById('newton-method-select');
    const note = document.getElementById('newton-method-note');
    if (select && note) {
        if (select.value === 'equidistant') {
            note.textContent = 'Mốc cách đều yêu cầu các giá trị x cách nhau một khoảng h không đổi.';
            note.style.display = 'block';
        } else {
             note.textContent = 'Mốc bất kỳ không yêu cầu các giá trị x cách đều.';
            note.style.display = 'block';
        }
    }
}

async function handleCentralInterpolationCalculation() {
    const xNodes = document.getElementById('central-x-nodes').value;
    const yNodes = document.getElementById('central-y-nodes').value;
    const methodType = document.getElementById('central-method-select').value;

    if (!xNodes.trim() || !yNodes.trim()) {
        showError('Vui lòng nhập đầy đủ các mốc x và giá trị y.');
        return;
    }

    showLoading();
    try {
        const data = await calculateCentralInterpolation(xNodes, yNodes, methodType);
        renderInterpolationSolution(document.getElementById('results-area'), data); // Dùng chung render
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

function updateCentralMethodNote() { // <<< THÊM HÀM NOTE (optional)
    const select = document.getElementById('central-method-select');
    // Add logic here if you want to display specific notes based on the selected central method (Gauss I/II, Stirling, Bessel)
    // For now, it does nothing, but the structure is here.
    // Example:
    // const note = document.getElementById('central-method-note');
    // if (select && note) {
    //     if (select.value === 'gauss_i' || select.value === 'gauss_ii') {
    //         note.textContent = 'Phương pháp Gauss yêu cầu số mốc lẻ.';
    //         note.style.display = 'block';
    //     } else {
    //         note.textContent = 'Phương pháp Stirling/Bessel yêu cầu số mốc chẵn.';
    //         note.style.display = 'block';
    //     }
    // }
}
