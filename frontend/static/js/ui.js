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
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    // 1. Tiêu đề và thông báo trạng thái
    let html = `<h2 class="result-heading">Kết quả - ${data.method}</h2>`;
    html += `<p class="text-center font-semibold text-lg mb-6 ${
        data.status === 'unique_solution' ? 'text-green-600' : 'text-orange-600'
    }">${data.message}</p>`;

    // 2. Hiển thị thông báo chuyển đổi (dành riêng cho Cholesky)
    if (data.method === "Cholesky" && data.transformation_message) {
        html += `<p class="text-center text-sm text-gray-600 italic mb-6">${data.transformation_message}</p>`;
    }

    // 3. Hiển thị các ma trận phân rã (cho LU và Cholesky)
    if (data.decomposition) {
        // Ma trận M, d (Cholesky, nếu A không đối xứng)
        if (data.decomposition.M) {
            html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-2">Hệ phương trình tương đương (M = AᵀA, d = Aᵀb):</h3>`;
            html += `<div class="flex flex-wrap items-center justify-center gap-4">`;
            html += `<div class="matrix-display">${formatMatrix(data.decomposition.M, 'M')}</div>`;
            html += `<div class="matrix-display">${formatMatrix(data.decomposition.d, 'd')}</div>`;
            html += `</div>`;
        }

        // Ma trận P, L, U (cho LU)
        if (data.method === "Phân rã LU") {
            html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-2">Các ma trận phân rã (P*A = L*U):</h3>`;
            html += `<div class="flex flex-wrap items-center justify-center gap-4">`;
            if (data.decomposition.P) html += `<div class="matrix-display">${formatMatrix(data.decomposition.P, 'P')}</div>`;
            if (data.decomposition.L) html += `<div class="matrix-display">${formatMatrix(data.decomposition.L, 'L')}</div>`;
            if (data.decomposition.U) html += `<div class="matrix-display">${formatMatrix(data.decomposition.U, 'U')}</div>`;
            html += `</div>`;
        }

        // Ma trận U, Uᵀ (cho Cholesky)
        if (data.method === "Cholesky") {
            html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-2">Phân rã Cholesky (M = UᵀU):</h3>`;
            html += `<div class="flex flex-wrap items-center justify-center gap-4">`;
            if (data.decomposition.Ut) html += `<div class="matrix-display">${formatMatrix(data.decomposition.Ut, 'Uᵀ')}</div>`;
            if (data.decomposition.U) html += `<div class="matrix-display">${formatMatrix(data.decomposition.U, 'U')}</div>`;
            html += `</div>`;
        }
    }
    
    // 4. Hiển thị vector trung gian Y (cho LU và Cholesky)
    if (data.intermediate_y) {
         html += `
            <div class="mt-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Vector trung gian (Y):</h3>
                <div class="matrix-display">${formatMatrix(data.intermediate_y, 'Y')}</div>
            </div>`;
    }

    // 5. Hiển thị nghiệm chính
    if (data.status === 'unique_solution' && data.solution) {
        html += `
            <div class="my-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Nghiệm duy nhất (X):</h3>
                <div class="matrix-display">${formatMatrix(data.solution, 'X')}</div>
            </div>`;
    } else if (data.status === 'infinite_solutions' && data.general_solution) {
        html += `
            <div class="my-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Nghiệm tổng quát:</h3>
                <div class="matrix-display">${formatGeneralSolution(data.general_solution)}</div>
            </div>`;
    }

    // 6. Hiển thị các bước trung gian (tùy theo phương pháp)
    if (data.method === "Phân rã LU" && data.steps && data.steps.length > 0) {
        html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-2">Các bước phân rã LU (không pivoting):</h3>`;
        data.steps.forEach(step => {
            html += `<div class="mb-4 p-3 bg-gray-50 rounded-lg shadow-sm">`;
            html += `<p class="text-sm text-gray-800 mb-2">${step.message}</p>`;
            html += `<div class="flex flex-wrap items-center justify-center gap-4">`;
            html += `<div class="matrix-display">${formatMatrix(step.L, 'L')}</div>`;
            html += `<div class="matrix-display">${formatMatrix(step.U, 'U')}</div>`;
            html += `</div></div>`;
        });
    } else if ((data.method === "Khử Gauss" || data.method === "Gauss-Jordan") && data.steps && data.steps.length > 0) {
        html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-4">Các bước khử:</h3>`;
        data.steps.forEach(step => {
            html += `
                <div class="mb-4 p-3 bg-gray-50 rounded-lg shadow-sm">
                    <p class="text-sm text-gray-800 mb-2">${step.message}</p>
                    <div class="matrix-display">${formatMatrix(step.matrix, '', step.num_vars)}</div>
                </div>`;
        });
    }
    
    // 7. Hiển thị các bước thế ngược (dành riêng cho Gauss)
    if (data.method === "Khử Gauss" && data.status === 'unique_solution' && data.backward_steps && data.backward_steps.length > 0) {
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

/**
 * Hiển thị kết quả tính ma trận nghịch đảo.
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu kết quả từ API.
 */
export function renderInverse(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    // 1. Tiêu đề và thông báo trạng thái
    let html = `<h2 class="result-heading">Kết quả - ${data.method}</h2>`;
    html += `<p class="text-center font-semibold text-lg mb-6 text-green-600">${data.message}</p>`;

    // 2. Hiển thị ma trận nghịch đảo
    if (data.inverse) {
        html += `
            <div class="mt-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Ma trận nghịch đảo (A⁻¹):</h3>
                <div class="matrix-display">${formatMatrix(data.inverse, 'A⁻¹')}</div>
            </div>`;
    }

    // 3. Hiển thị các bước tính toán
    if (data.steps && data.steps.length > 0) {
        html += `<h3 class="text-lg font-semibold text-gray-700 my-4">Các bước tính toán:</h3>`;
        data.steps.forEach((step, index) => {
            html += `
                <div class="mb-4 p-3 bg-blue-50 rounded-lg shadow-sm">
                    <p class="text-sm text-gray-800 mb-2">${step.message}</p>
                    <div class="matrix-display">${formatMatrix(step.matrix, '', step.num_vars)}</div>
                </div>`;
        });
    }

    container.innerHTML = html;
}