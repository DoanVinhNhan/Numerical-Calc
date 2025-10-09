// frontend/static/js/handlers/direct_methods_handler.js
import { solveLinearSystem } from '../api.js';
import { renderMatrixSolution, showLoading, hideLoading, showError } from '../ui.js';

/**
 * Thiết lập các trình xử lý sự kiện cho các phương pháp giải trực tiếp.
 * Hàm này tìm các nút bấm trong DOM và gắn sự kiện 'click' cho chúng.
 */
export function setupDirectMethodsHandlers() {
    // Gắn sự kiện cho nút tính toán Gauss
    const calculateGaussBtn = document.getElementById('calculate-gauss-btn');
    if (calculateGaussBtn) {
        calculateGaussBtn.addEventListener('click', handleGaussCalculation);
    }
    
    const calculateGJButton = document.getElementById('calculate-gj-btn');
    if (calculateGJButton) {
        calculateGJButton.addEventListener('click', handleGaussJordanCalculation);
    }
    const calculateLUBtn = document.getElementById('calculate-lu-btn');
    if (calculateLUBtn) {
        calculateLUBtn.addEventListener('click', handleLuCalculation);
    }
    const calculateCholeskyBtn = document.getElementById('calculate-cholesky-btn');
    if (calculateCholeskyBtn) {
        calculateCholeskyBtn.addEventListener('click', handleCholeskyCalculation);
    }
}

/**
 * Xử lý yêu cầu tính toán bằng phương pháp khử Gauss.
 * Đây là một hàm bất đồng bộ vì nó đợi kết quả trả về từ API.
 */
async function handleGaussCalculation() {
    // Lấy giá trị từ các ô input trên trang
    const matrixA = document.getElementById('matrix-a-input-hpt').value;
    const matrixB = document.getElementById('matrix-b-input-hpt').value;
    const zeroTolerance = document.getElementById('setting-zero-tolerance').value;
    const resultsArea = document.getElementById('results-area');

    // Hiển thị chỉ báo đang tải và xóa kết quả cũ
    showLoading();
    
    try {
        // Gọi hàm API để giải hệ phương trình, truyền vào các giá trị đã thu thập
        const data = await solveLinearSystem('gauss', matrixA, matrixB, zeroTolerance);
        
        // Nếu thành công, hiển thị kết quả
        renderMatrixSolution(resultsArea, data);
    } catch (error) {
        // Nếu có lỗi, hiển thị thông báo lỗi
        showError(error.message);
    } finally {
        // Dù thành công hay thất bại, luôn ẩn chỉ báo đang tải khi hoàn tất
        hideLoading();
    }
}

async function handleGaussJordanCalculation() {
    const matrixA = document.getElementById('matrix-a-input-hpt').value;
    const matrixB = document.getElementById('matrix-b-input-hpt').value;
    const zeroTolerance = document.getElementById('setting-zero-tolerance').value;
    const resultsArea = document.getElementById('results-area');

    showLoading();
    
    try {
        // Gọi API với method là 'gauss-jordan'
        const data = await solveLinearSystem('gauss-jordan', matrixA, matrixB, zeroTolerance);
        renderMatrixSolution(resultsArea, data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function handleLuCalculation() {
    const matrixA = document.getElementById('matrix-a-input-hpt').value;
    const matrixB = document.getElementById('matrix-b-input-hpt').value;
    const zeroTolerance = document.getElementById('setting-zero-tolerance').value;
    const resultsArea = document.getElementById('results-area');

    showLoading();
    
    try {
        const data = await solveLinearSystem('lu', matrixA, matrixB, zeroTolerance);
        renderMatrixSolution(resultsArea, data); // Dùng lại hàm render cũ
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function handleCholeskyCalculation() {
    const matrixA = document.getElementById('matrix-a-input-hpt').value;
    const matrixB = document.getElementById('matrix-b-input-hpt').value;
    const zeroTolerance = document.getElementById('setting-zero-tolerance').value;
    const resultsArea = document.getElementById('results-area');

    showLoading();
    
    try {
        const data = await solveLinearSystem('cholesky', matrixA, matrixB, zeroTolerance);
        renderMatrixSolution(resultsArea, data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}