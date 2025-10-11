// frontend/static/js/ui.js
import {formatCell, formatMatrix, formatGeneralSolution } from './formatters.js';

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

    let html = `<h2 class="result-heading">Kết quả - ${data.method}</h2>`;
    html += `<p class="text-center font-semibold text-lg mb-6 text-green-600">${data.message}</p>`;

    if (data.inverse) {
        html += `
            <div class="my-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Ma trận nghịch đảo (A⁻¹):</h3>
                <div class="matrix-display">${formatMatrix(data.inverse, 'A⁻¹')}</div>
            </div>`;
    }

    if (data.steps && data.steps.length > 0) {
        html += `<h3 class="text-lg font-semibold text-gray-700 my-4">Các bước tính toán:</h3>`;
        data.steps.forEach(step => {
            html += `
                <div class="mb-4 p-3 bg-blue-50 rounded-lg shadow-sm">
                    <p class="text-sm text-gray-800 mb-2">${step.message}</p>`;

            // Vùng hiển thị ma trận
            html += `<div class="flex flex-wrap items-center justify-center gap-4">`;
            
            if (step.M) html += `<div class="matrix-display">${formatMatrix(step.M, 'M')}</div>`;

            // Hiển thị các ma trận phân rã P, L, U
            if (step.P) html += `<div class="matrix-display">${formatMatrix(step.P, 'P')}</div>`;
            if (step.L) html += `<div class="matrix-display">${formatMatrix(step.L, 'L')}</div>`;
            if (step.U) html += `<div class="matrix-display">${formatMatrix(step.U, 'U')}</div>`;
            
            // Hiển thị ma trận kết quả của một bước (nếu có)
            if (step.matrix) html += `<div class="matrix-display">${formatMatrix(step.matrix, '', step.num_vars)}</div>`;
            
            // Hiển thị các vector cột trong quá trình giải
            if (step.solve_process) {
                 html += `<div class="w-full text-center text-sm my-2 font-mono">${step.solve_process}</div>`;
            }
            if (step.Y_col) html += `<div class="matrix-display">${formatMatrix(step.Y_col, 'Y')}</div>`;
            if (step.X_col) html += `<div class="matrix-display">${formatMatrix(step.X_col, 'X')}</div>`;

            html += `</div></div>`;
        });
    }

    container.innerHTML = html;
}

/**
 * Hiển thị kết quả của các phương pháp lặp (Jacobi, Gauss-Seidel, Lặp Đơn).
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu kết quả từ API.
 */
export function renderIterativeSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    let html = `<h2 class="result-heading">Kết quả - ${data.method}</h2>`;
    html += `<p class="text-center font-semibold text-lg mb-6 text-green-600">${data.message}</p>`;

    // Hiển thị thông tin hội tụ
    if (data.convergence_info) {
        const { dominance_type, norm_used, contraction_coefficient, coeff_q, coeff_s, warning_message, stopping_threshold} = data.convergence_info;
        
        let convergenceHtml = `<div class="mb-4 p-3 bg-gray-50 rounded-lg text-center">`;
        if (dominance_type) {
            convergenceHtml += `<p class="text-sm">${dominance_type}. ${norm_used}.</p>`;
        }
        if (contraction_coefficient !== undefined) {
             convergenceHtml += `<p class="text-sm">Hệ số co $||B||$ = <strong>${contraction_coefficient.toFixed(6)}</strong></p>`;
        }
        if (coeff_q !== undefined && coeff_s !== undefined) {
            convergenceHtml += `<p class="text-sm">Hệ số co: $q$ = <strong>${coeff_q.toFixed(6)}</strong>, $s$ = <strong>${coeff_s.toFixed(6)}</strong></p>`;
        }
        if (stopping_threshold !== undefined && data.method === "Lặp Đơn") {
            convergenceHtml += `<p class="text-sm">Điều kiện dừng: $||X_k - X_{k-1}|| < ${stopping_threshold.toExponential(4)}$</p>`;
        }
        if (warning_message) {
            convergenceHtml += `<p class="text-sm text-red-600 font-semibold mt-2">${warning_message}</p>`;
        }
        convergenceHtml += `</div>`;
        html += convergenceHtml;
    }

    // Hiển thị nghiệm
    if (data.solution) {
        html += `
            <div class="my-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Nghiệm của hệ phương trình (X):</h3>
                <div class="matrix-display">${formatMatrix(data.solution, 'X')}</div>
            </div>`;
    }

    // Hiển thị bảng lặp
    if (data.steps && data.steps[0].table) {
        const table = data.steps[0].table;
        
        const normSymbol = (data.convergence_info?.norm_used === "infinity" || data.convergence_info?.norm_used === 'inf') ? '\\infty' : '1';
        const diffNormFormula = `\\|X_k - X_{k-1}\\|_{${normSymbol}}`;
        let errorColName = "Sai số ước tính";

        if (data.method === "Lặp Đơn") {
            errorColName = `$${diffNormFormula}$`;
        } else if (data.method === "Lặp Jacobi") {
            const q = data.convergence_info?.contraction_coefficient;
            errorColName = q < 1 ? `$\\frac{q}{1-q}${diffNormFormula}$` : `$${diffNormFormula}$ (q \\ge 1)`;
        } else if (data.method === "Lặp Gauss-Seidel") {
             errorColName = `$\\frac{q}{(1-s)(1-q)}${diffNormFormula}$`;
        }
        
        const diffColName = (data.method !== "Lặp Đơn") ? `$${diffNormFormula}$` : "";

        html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-4">Bảng quá trình lặp:</h3>`;
        html += `<div class="overflow-x-auto"><table class="w-full text-sm text-left text-gray-700">`;
        html += `<thead class="text-xs text-gray-800 bg-gray-100"><tr>
            <th scope="col" class="px-6 py-3">$k$</th>
            <th scope="col" class="px-6 py-3">$X_k$</th>
            ${diffColName ? `<th scope="col" class="px-6 py-3">${diffColName}</th>` : ''}
            <th scope="col" class="px-6 py-3">${errorColName}</th>
        </tr></thead><tbody>`;

        table.forEach(row => {
            const error_val = row.error === null || row.error === undefined ? 'N/A' : row.error.toExponential(4);
            const diff_norm_val = row.diff_norm !== undefined ? row.diff_norm.toExponential(4) : '';

            html += `<tr class="bg-white border-b">
                <td class="px-6 py-4 font-medium">${row.k}</td>
                <td class="px-6 py-4">${formatMatrix(row.x_k)}</td>
                ${diffColName ? `<td class="px-6 py-4 font-mono">${diff_norm_val}</td>` : ''}
                <td class="px-6 py-4 font-mono">${error_val}</td>
            </tr>`;
        });

        html += `</tbody></table></div>`;
    }

    container.innerHTML = html;

    // Sau khi chèn HTML, tìm và render tất cả các công thức toán học
    if (window.katex) {
        container.querySelectorAll('th, p').forEach(elem => {
            const matches = elem.innerHTML.match(/\$(.*?)\$/g);
            if (matches) {
                matches.forEach(match => {
                    const formula = match.slice(1, -1).replace(/&lt;/g, '<').replace(/&gt;/g, '>');
                    try {
                        const renderedFormula = katex.renderToString(formula, {
                            throwOnError: false,
                            displayMode: false
                        });
                        elem.innerHTML = elem.innerHTML.replace(match, renderedFormula);
                    } catch (e) {
                        // Bỏ qua lỗi render
                    }
                });
            }
        });
    }
}


/**
 * Hiển thị kết quả tính ma trận nghịch đảo bằng phương pháp lặp.
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu kết quả từ API.
 */
export function renderInverseIterativeSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    let html = `<h2 class="result-heading">Kết quả - ${data.method}</h2>`;
    html += `<p class="text-center font-semibold text-lg mb-6 text-green-600">${data.message}</p>`;

    // Hiển thị thông tin hội tụ
    if (data.convergence_info) {
        const { dominance_type, norm_used, contraction_coefficient, coeff_q, coeff_s, x0_label } = data.convergence_info;
        html += `<div class="mb-4 p-3 bg-gray-50 rounded-lg text-center text-sm">`;
        if (dominance_type) {
            html += `<p>${dominance_type}.</p>`;
        }
        if (norm_used) {
            html += `<p>${norm_used}.</p>`;
        }
        
        // Kiểm tra và hiển thị hệ số co tương ứng
        if (contraction_coefficient !== undefined) {
             html += `<p>Hệ số co q = <strong>${contraction_coefficient.toFixed(6)}</strong>.</p>`;
        }
        if (coeff_q !== undefined && coeff_s !== undefined) {
             html += `<p>Hệ số: q = <strong>${coeff_q.toFixed(6)}</strong>, s = <strong>${coeff_s.toFixed(6)}</strong>.</p>`;
        }
        
        if (x0_label) {
            html += `<p>Ma trận ban đầu: ${x0_label}</p>`;
        }
        html += `</div>`;
    }

    // Hiển thị ma trận ban đầu X₀
    if (data.initial_matrix) {
        html += `
            <div class="my-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Ma trận lặp ban đầu (X₀):</h3>
                <div class="matrix-display">${formatMatrix(data.initial_matrix, 'X₀')}</div>
            </div>`;
    }

    // Ma trận nghịch đảo và ma trận kiểm tra
    html += `<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
        <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-2">Ma trận nghịch đảo (A⁻¹):</h3>
            <div class="matrix-display">${formatMatrix(data.inverse, 'A⁻¹')}</div>
        </div>
        <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-2">Kiểm tra (A * A⁻¹ ≈ I):</h3>
            <div class="matrix-display">${formatMatrix(data.check_matrix, 'Check')}</div>
        </div>
    </div>`;

    // Bảng quá trình lặp
    if (data.steps && data.steps[0].table) {
        const table = data.steps[0].table;
        let normSymbol, diffNormFormula, errorColName;
        
        const q_val = data.convergence_info?.coeff_q ?? data.convergence_info?.contraction_coefficient;

        if (data.method.includes("Newton")) {
            normSymbol = '2';
            diffNormFormula = `\\|X_k - X_{k-1}\\|_{${normSymbol}}`;
            errorColName = q_val < 1 ? `$\\frac{q}{1-q}${diffNormFormula}$` : `$${diffNormFormula}$ (q \\ge 1)`;
        } else { // Jacobi hoặc Gauss-Seidel
            normSymbol = data.convergence_info?.norm_used === "infinity" ? '\\infty' : '1';
            diffNormFormula = `\\|X_k - X_{k-1}\\|_{${normSymbol}}`;
            
            if (data.method.includes("Gauss-Seidel")) {
                const s_val = data.convergence_info?.coeff_s;
                errorColName = `$\\frac{q}{(1-s)(1-q)}${diffNormFormula}$`;
            } else { // Jacobi
                errorColName = q_val < 1 ? `$\\frac{q}{1-q}${diffNormFormula}$` : `$${diffNormFormula}$ (q \\ge 1)`;
            }
        }

        html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-4">Bảng quá trình lặp:</h3>`;
        html += `<div class="overflow-x-auto"><table class="w-full text-sm text-left text-gray-700">
            <thead class="text-xs text-gray-800 bg-gray-100"><tr>
                <th scope="col" class="px-6 py-3">$k$</th>
                <th scope="col" class="px-6 py-3">$X_k$</th>
                <th scope="col" class="px-6 py-3">$${diffNormFormula}$</th>
                <th scope="col" class="px-6 py-3">${errorColName}</th>
            </tr></thead><tbody>`;

        const maxRowsToShow = 10;
        const totalRows = table.length;
        
        table.forEach((row, index) => {
            const error_val = (row.error !== undefined && row.error !== null) ? row.error.toExponential(4) : 'N/A';
            const estimated_error_val = (row.estimated_error !== undefined && row.estimated_error !== null) ? row.estimated_error.toExponential(4) : 'N/A';

            const rowClass = (totalRows > maxRowsToShow && index >= maxRowsToShow / 2 && index < totalRows - maxRowsToShow / 2) ? 'iteration-row-hidden' : '';
            html += `<tr class="bg-white border-b ${rowClass}">
                <td class="px-6 py-4 font-medium">${row.k}</td>
                <td class="px-6 py-4">${formatMatrix(row.x_k)}</td>
                <td class="px-6 py-4 font-mono">${error_val}</td>
                <td class="px-6 py-4 font-mono">${estimated_error_val}</td>
            </tr>`;
        });
        
        if (totalRows > maxRowsToShow) {
            html += `<tr class="toggle-row"><td colspan="4" class="text-center"><button class="toggle-table-btn" onclick="this.closest('table').querySelectorAll('.iteration-row-hidden').forEach(r => r.style.display = r.style.display === 'none' ? 'table-row' : 'none'); this.textContent = this.textContent.includes('Xem') ? 'Ẩn bớt' : 'Xem thêm ${totalRows - maxRowsToShow} hàng...';">Xem thêm ${totalRows - maxRowsToShow} hàng...</button></td></tr>`;
        }

        html += `</tbody></table></div>`;
    }

    container.innerHTML = html;
    if (window.katex) {
        container.querySelectorAll('th, p').forEach(elem => {
            const matches = elem.innerHTML.match(/\$(.*?)\$/g);
            if (matches) {
                matches.forEach(match => {
                    const formula = match.slice(1, -1).replace(/&lt;/g, '<').replace(/&gt;/g, '>');
                    try {
                        const renderedFormula = katex.renderToString(formula, { throwOnError: false, displayMode: false });
                        elem.innerHTML = elem.innerHTML.replace(match, renderedFormula);
                    } catch (e) { /* Bỏ qua lỗi render */ }
                });
            }
        });
    }
}

export function renderSvdSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    let html = `<h2 class="result-heading">Kết quả - Phân tích SVD (${data.method})</h2>`;
    
    html += `<h3 class="text-xl font-semibold text-gray-700 mt-6 mb-2 text-center">A ≈ UΣVᵀ</h3>`;
    html += `<div class="flex flex-wrap items-center justify-center gap-4">
        <div class="matrix-display">${formatMatrix(data.U, 'U')}</div>
        <div class="matrix-display">${formatMatrix(data.Sigma, 'Σ')}</div>
        <div class="matrix-display">${formatMatrix(data.Vt, 'Vᵀ')}</div>
    </div>`;

    if (data.intermediate_steps && data.intermediate_steps.steps) {
        const steps = data.intermediate_steps.steps;
        html += `<h3 class="text-xl font-semibold text-gray-700 mt-8 mb-4">Các bước trung gian (Power Method)</h3>`;
        html += `<p class="text-center text-sm text-gray-600 mb-4">Làm việc với ma trận: <strong>${data.intermediate_steps.matrix_used_info}</strong></p>`;

        steps.forEach(step => {
            html += `<div class="mb-6 p-4 bg-gray-50 rounded-lg shadow-sm border">
                <h4 class="text-lg font-semibold text-blue-700 mb-3">Tìm giá trị kỳ dị thứ ${step.singular_index} (σ = ${step.singular_value.toFixed(4)})</h4>
                
                <p class="text-sm mb-2"><strong>1. Dùng Power Method</strong> trên ma trận B<sub>${step.singular_index - 1}</sub> để tìm giá trị riêng lớn nhất λ = ${step.eigenvalue.toFixed(4)} và vector riêng tương ứng.</p>
                <details class="mb-3">
                    <summary class="cursor-pointer text-sm text-blue-600 hover:underline">Xem chi tiết ${step.lambda_steps.length} bước lặp Power Method</summary>
                    <div class="overflow-x-auto mt-2"><table class="w-full text-sm">
                        <thead class="bg-gray-200"><tr><th class="p-2">k</th><th class="p-2">Vector yₖ</th><th class="p-2">λₖ</th></tr></thead>
                        <tbody>`;
            step.lambda_steps.forEach((lambda, i) => {
                html += `<tr class="border-b"><td class="p-2">${i + 1}</td><td class="p-2 font-mono">${formatMatrix(step.y_steps[i+1])}</td><td class="p-2 font-mono">${lambda.toFixed(6)}</td></tr>`;
            });
            html += `</tbody></table></div>
                </details>

                <p class="text-sm mb-2"><strong>2. Quá trình Deflation:</strong> B<sub>${step.singular_index}</sub> = B<sub>${step.singular_index - 1}</sub> - λ * v * vᵀ</p>
                <div class="flex flex-wrap items-start justify-center gap-4">
                    <div><p class="text-xs text-center font-semibold">B<sub>${step.singular_index-1}</sub> (Trước)</p><div class="matrix-display">${formatMatrix(step.matrix_before_deflation)}</div></div>
                    <div><p class="text-xs text-center font-semibold">B<sub>${step.singular_index}</sub> (Sau)</p><div class="matrix-display">${formatMatrix(step.matrix_after_deflation)}</div></div>
                </div>
            </div>`;
        });
    }

    container.innerHTML = html;
}

function formatComplexNumber(num, precision = 4) {
    if (typeof num === 'number') {
        return num.toFixed(precision);
    }
    if (num && typeof num.real === 'number' && typeof num.imag === 'number') {
        if (Math.abs(num.imag) < 1e-9) return num.real.toFixed(precision);
        const imagSign = num.imag > 0 ? '+' : '-';
        return `${num.real.toFixed(precision)} ${imagSign} ${Math.abs(num.imag).toFixed(precision)}i`;
    }
    return num;
}

export function renderEigenSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    let html = `<h2 class="result-heading">Kết quả - ${data.method}</h2>`;

    // Đa thức đặc trưng
    let polyHtml = 'P(λ) = ';
    const degree = data.char_poly.length - 1;
    data.char_poly.forEach((coeff, i) => {
        const coeffVal = (typeof coeff === 'number') ? coeff : coeff.real;
        if (Math.abs(coeffVal) < 1e-9 && degree - i !== 0) return;
        
        let sign = i > 0 ? (coeffVal >= 0 ? ' + ' : ' - ') : (coeffVal >= 0 ? '' : '- ');

        let coeffStr = Math.abs(coeffVal).toFixed(4);
        const power = degree - i;
        if (Math.abs(parseFloat(coeffStr) - 1) < 1e-9 && power > 0) {
            coeffStr = '';
        }

        polyHtml += `${sign}${coeffStr}`;
        if (power > 1) polyHtml += `λ<sup>${power}</sup>`;
        else if (power === 1) polyHtml += `λ`;
    });
    html += `<div class="my-4 p-3 bg-gray-100 rounded-lg text-center font-mono text-lg">${polyHtml} = 0</div>`;

    // Bảng trị riêng, vector riêng và kiểm tra
    html += `<h3 class="text-xl font-semibold text-gray-700 mt-6 mb-2">Trị riêng và Vector riêng</h3>`;
    html += `<div class="overflow-x-auto"><table class="w-full text-sm">
        <thead class="bg-gray-200"><tr>
            <th class="p-2">Trị riêng (λ)</th>
            <th class="p-2">Vector riêng (v)</th>
            <th class="p-2">Kiểm tra (Av ≈ λv)</th>
        </tr></thead><tbody>`;

    data.eigen_pairs.forEach(pair => {
        html += `<tr class="border-b">
            <td class="p-2 font-mono text-center">${formatCell(pair.lambda, 4)}</td>
            <td class="p-2">${formatMatrix(pair.v)}</td>
            <td class="p-2">
                <div class="flex flex-wrap items-center justify-center gap-x-4 gap-y-2">
                    <div class="text-center">
                        <span class="text-xs font-semibold">Av</span>
                        ${formatMatrix(pair.Av_check)}
                    </div>
                    <div class="font-bold text-lg">≈</div>
                    <div class="text-center">
                        <span class="text-xs font-semibold">λv</span>
                        ${formatMatrix(pair.lambda_v_check)}
                    </div>
                </div>
            </td>
        </tr>`;
    });
    html += `</tbody></table></div>`;

    // Các bước trung gian
    html += `<h3 class="text-xl font-semibold text-gray-700 mt-8 mb-4">Các bước biến đổi Danilevsky</h3>`;
    data.steps.forEach(step => {
        html += `<div class="mb-4 p-3 bg-gray-50 rounded-lg shadow-sm border">
            <p class="text-sm font-medium text-gray-800 mb-2">${step.desc}</p>
            <div class="matrix-display">${formatMatrix(step.matrix)}</div>
        </div>`;
    });

    container.innerHTML = html;
}