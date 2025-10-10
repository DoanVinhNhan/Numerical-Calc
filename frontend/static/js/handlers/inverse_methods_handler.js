// frontend/static/js/handlers/inverse_methods_handler.js
import { calculateInverse } from '../api.js';
import { renderInverse, showLoading, hideLoading, showError } from '../ui.js';

/**
 * Thiết lập các trình xử lý sự kiện cho các phương pháp tính ma trận nghịch đảo.
 * Hàm này tìm các nút bấm trong DOM và gắn sự kiện 'click' cho chúng.
 */
export function setupInverseMethodsHandlers() {
    // Gắn sự kiện cho nút tính ma trận nghịch đảo Gauss-Jordan
    const calculateGaussJordanInverseBtn = document.getElementById('calculate-inv-gj-btn');
    if (calculateGaussJordanInverseBtn) {
        calculateGaussJordanInverseBtn.addEventListener('click', handleGaussJordanInverseCalculation);
    }
    const calculateLUInverseBtn = document.getElementById('calculate-inv-lu-btn');
    if (calculateLUInverseBtn) {
        calculateLUInverseBtn.addEventListener('click', handleLUInverseCalculation);
    }
    const calculateCholeskyInverseBtn = document.getElementById('calculate-inv-cholesky-btn');
    if (calculateCholeskyInverseBtn) {
        calculateCholeskyInverseBtn.addEventListener('click', handleCholeskyInverseCalculation);
    }
    const calculateBorderingInverseBtn = document.getElementById('calculate-inv-bordering-btn');
    if (calculateBorderingInverseBtn) {
        calculateBorderingInverseBtn.addEventListener('click', handleBorderingInverseCalculation);
    }
}

/**
 * Xử lý yêu cầu tính ma trận nghịch đảo bằng phương pháp Gauss-Jordan.
 * Đây là một hàm bất đồng bộ vì nó đợi kết quả trả về từ API.
 */
async function handleGaussJordanInverseCalculation() {
    // Lấy giá trị từ các ô input trên trang
    const matrixA = document.getElementById('matrix-a-input-inv-direct').value;
    const zeroTolerance = document.getElementById('setting-zero-tolerance').value;
    const resultsArea = document.getElementById('results-area');

    // Kiểm tra đầu vào
    if (!matrixA.trim()) {
        showError('Vui lòng nhập ma trận A.');
        return;
    }

    // Hiển thị chỉ báo đang tải và xóa kết quả cũ
    showLoading();
    
    try {
        // Gọi hàm API để tính ma trận nghịch đảo
        const data = await calculateInverse('gauss-jordan', matrixA, zeroTolerance);
        
        // Nếu thành công, hiển thị kết quả
        renderInverse(resultsArea, data);
    } catch (error) {
        // Nếu có lỗi, hiển thị thông báo lỗi
        console.error('Lỗi khi tính ma trận nghịch đảo:', error);
        showError(error.message || 'Đã xảy ra lỗi khi tính ma trận nghịch đảo.');
    } finally {
        // Luôn luôn ẩn chỉ báo tải khi hoàn thành
        hideLoading();
    }
}

async function handleLUInverseCalculation() {
    const matrixA = document.getElementById('matrix-a-input-inv-direct').value;
    const zeroTolerance = document.getElementById('setting-zero-tolerance').value;
    const resultsArea = document.getElementById('results-area');

    if (!matrixA.trim()) {
        showError('Vui lòng nhập ma trận A.');
        return;
    }

    showLoading();
    
    try {
        const data = await calculateInverse('lu', matrixA, zeroTolerance);
        renderInverse(resultsArea, data); // Dùng lại hàm renderInverse
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function handleCholeskyInverseCalculation() {
    const matrixA = document.getElementById('matrix-a-input-inv-direct').value;
    const zeroTolerance = document.getElementById('setting-zero-tolerance').value;
    const resultsArea = document.getElementById('results-area');

    if (!matrixA.trim()) {
        showError('Vui lòng nhập ma trận A.');
        return;
    }

    showLoading();
    
    try {
        const data = await calculateInverse('cholesky', matrixA, zeroTolerance);
        renderInverse(resultsArea, data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function handleBorderingInverseCalculation() {
    const matrixA = document.getElementById('matrix-a-input-inv-direct').value;
    const zeroTolerance = document.getElementById('setting-zero-tolerance').value;
    const resultsArea = document.getElementById('results-area');

    if (!matrixA.trim()) {
        showError('Vui lòng nhập ma trận A.');
        return;
    }

    showLoading();
    
    try {
        // Gọi API với method 'bordering'
        const data = await calculateInverse('bordering', matrixA, zeroTolerance);
        renderInverse(resultsArea, data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}