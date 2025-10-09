// frontend/static/js/ui.js
import { formatMatrix, formatGeneralSolution } from './formatters.js';

// KHÔNG khai báo biến const ở đây nữa.

/** Hiển thị chỉ báo đang tải */
export function showLoading() {
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorMessageDiv = document.getElementById('error-message');
    const resultsArea = document.getElementById('results-area');

    if (loadingSpinner) loadingSpinner.classList.remove('hidden');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');
    if (resultsArea) resultsArea.innerHTML = ''; // Xóa kết quả cũ
}

/** Ẩn chỉ báo đang tải */
export function hideLoading() {
    const loadingSpinner = document.getElementById('loading-spinner');
    if (loadingSpinner) loadingSpinner.classList.add('hidden');
}

/**
 * Hiển thị thông báo lỗi.
 * @param {string} message - Nội dung lỗi cần hiển thị.
 */
export function showError(message) {
    const errorMessageDiv = document.getElementById('error-message');
    const resultsArea = document.getElementById('results-area');

    if (errorMessageDiv) {
        errorMessageDiv.textContent = message;
        errorMessageDiv.classList.remove('hidden');
    }
    if (resultsArea) resultsArea.innerHTML = ''; // Xóa kết quả nếu có lỗi
}

/**
 * Hiển thị kết quả giải hệ phương trình.
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu kết quả từ API.
 */
export function renderMatrixSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden'); // Ẩn lỗi cũ khi có kết quả mới

    // ... (Phần còn lại của hàm không đổi)
    let html = `<h2 class="result-heading">Kết quả - ${data.method}</h2>`;
    html += `<p class="text-center font-semibold text-lg mb-6 ${
        data.status === 'unique_solution' ? 'text-green-600' : 'text-orange-600'
    }">${data.message}</p>`;

    if (data.status === 'unique_solution' && data.solution) {
        html += `
            <div class="mb-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Nghiệm duy nhất (X):</h3>
                <div class="matrix-display">${formatMatrix(data.solution, 'X')}</div>
            </div>`;
    } else if (data.status === 'infinite_solutions' && data.general_solution) {
        html += `
            <div class="mb-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Nghiệm tổng quát:</h3>
                <div class="matrix-display">${formatGeneralSolution(data.general_solution)}</div>
            </div>`;
    }

    if (data.steps && data.steps.length > 0) {
        html += `<h3 class="text-lg font-semibold text-gray-700 mb-4">Các bước khử xuôi:</h3>`;
        data.steps.forEach(step => {
            html += `
                <div class="mb-4 p-3 bg-gray-50 rounded-lg shadow-sm">
                    <p class="text-sm text-gray-800 mb-2">${step.message}</p>
                    <div class="matrix-display">${formatMatrix(step.matrix, '', step.num_vars)}</div> 
                </div>`; // <-- Thêm step.num_vars vào đây
        });
    }
    
    if (data.status === 'unique_solution' && data.backward_steps && data.backward_steps.length > 0) {
        html += `<h3 class="text-lg font-semibold text-gray-700 my-4">Các bước thế ngược:</h3>`;
         data.backward_steps.forEach((step, index) => {
            html += `
                <div class="mb-4 p-3 bg-blue-50 rounded-lg shadow-sm">
                    <p class="text-sm text-gray-800 mb-2"><b>Bước ${index + 1}:</b> ${step.message}</p>
                    <div class="matrix-display">${formatMatrix(step.solution_so_far, 'X')}</div>
                </div>`;
        });
    }

    container.innerHTML = html;
}