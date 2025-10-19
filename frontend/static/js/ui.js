// frontend/static/js/ui.js
import {format_poly_str_js, formatCell, formatMatrix, formatGeneralSolution, renderHornerDivisionTable, renderHornerReverseTable } from './formatters.js';

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

    if (data.message) {
        html += `<p class="text-center font-semibold text-lg mb-6 text-green-600">${data.message}</p>`;
    }

    // --- 1. Hiển thị Đa thức đặc trưng (cho Danilevsky) ---
    if (data.char_poly) {
        let polyHtml = 'P(λ) = ';
        const degree = data.char_poly.length - 1;
        data.char_poly.forEach((coeff, i) => {
            const power = degree - i;
            if (Math.abs(coeff.real) < 1e-9 && Math.abs(coeff.imag) < 1e-9) return;

            let coeffStr = formatComplexNumber(coeff, 2);
            if (i > 0) {
                 polyHtml += (coeff.real >= 0 && !coeffStr.startsWith('-')) ? ' + ' : ' ';
            }
            
            if (power > 1) {
                polyHtml += `${coeffStr}λ<sup>${power}</sup>`;
            } else if (power === 1) {
                polyHtml += `${coeffStr}λ`;
            } else {
                polyHtml += `${coeffStr}`;
            }
        });
        html += `<div class="my-6 text-center"><h3 class="text-lg font-semibold text-gray-700 mb-2">Đa thức đặc trưng:</h3><p class="text-lg font-mono">${polyHtml}</p></div>`;
    }

    // --- 2. Hiển thị các cặp Giá trị riêng và Vector riêng ---
    html += `<h3 class="text-xl font-semibold text-gray-800 my-6 text-center">Các cặp Giá trị riêng (λ) và Vector riêng (v)</h3>`;
    data.eigen_pairs.forEach((pair, index) => {
        html += `<div class="mb-8 p-4 bg-gray-50 rounded-lg shadow-sm border">
            <h4 class="text-lg font-semibold text-blue-700 mb-4">Cặp ${index + 1}: λ = ${formatComplexNumber(pair.lambda)}</h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
                <div>
                    <h5 class="text-md font-semibold text-gray-700 mb-2 text-center">Vector riêng (v)</h5>
                    <div class="matrix-display">${formatMatrix(pair.v, 'v')}</div>
                </div>
                <div class="md:col-span-2">
                     <h5 class="text-md font-semibold text-gray-700 mb-2 text-center">Kiểm tra: A*v ≈ λ*v</h5>
                     <div class="flex flex-wrap items-center justify-center gap-4">
                        <div class="matrix-display">${formatMatrix(pair.Av_check, 'A*v')}</div>
                        <span class="font-bold text-2xl">≈</span>
                        <div class="matrix-display">${formatMatrix(pair.lambda_v_check, 'λ*v')}</div>
                     </div>
                </div>
            </div>
        </div>`;
    });

    // --- 3. Hiển thị các bước trung gian ---
    if (data.steps && data.steps.length > 0) {
        html += `<h3 class="text-xl font-semibold text-gray-800 mt-8 mb-4 text-center">Các bước tính toán chi tiết</h3>`;
        
        if (data.method === "Danilevsky") {
            data.steps.forEach(step => {
                html += `<details class="mb-4"><summary class="cursor-pointer text-md font-medium text-gray-800 hover:text-blue-600">${step.desc}</summary>
                    <div class="mt-2 p-3 bg-blue-50 rounded-lg">
                        <div class="matrix-display">${formatMatrix(step.matrix)}</div>
                    </div>
                </details>`;
            });
        } else if (data.method.includes("Power Method (GTR Trội)")) { // Xử lý riêng cho GTR Trội
            html += `<div class="mb-6 p-4 bg-gray-50 rounded-lg shadow-sm border">
                <h4 class="text-lg font-semibold text-blue-700 mb-3">Bảng quá trình lặp</h4>
                <div class="overflow-x-auto mt-2"><table class="w-full text-sm">
                    <thead class="bg-gray-200"><tr><th class="p-2">k</th><th class="p-2">Vector xₖ</th><th class="p-2">Vector Axₖ</th><th class="p-2">λₖ</th></tr></thead>
                    <tbody>`;
            data.steps.forEach(detail => {
                html += `<tr class="border-b"><td class="p-2">${detail.k}</td><td class="p-2 font-mono">${formatMatrix(detail.x_k)}</td><td class="p-2 font-mono">${formatMatrix(detail.Ax_k)}</td><td class="p-2 font-mono">${detail.lambda_k.toFixed(6)}</td></tr>`;
            });
            html += `</tbody></table></div></div>`;
        } else if (data.method.includes("Power Method & Deflation")) { // Xử lý cho Xuống thang
            data.steps.forEach(step => {
                html += `<div class="mb-6 p-4 bg-gray-50 rounded-lg shadow-sm border">
                    <h4 class="text-lg font-semibold text-blue-700 mb-3">${step.desc}</h4>
                    <div class="matrix-display">${formatMatrix(step.matrix)}</div>
                    <details class="mt-3"><summary class="cursor-pointer text-sm text-blue-600 hover:underline">Xem chi tiết ${step.iteration_details.length} bước lặp Power Method</summary>
                        <div class="overflow-x-auto mt-2"><table class="w-full text-sm">
                            <thead class="bg-gray-200"><tr><th class="p-2">k</th><th class="p-2">Vector xₖ</th><th class="p-2">Vector Axₖ</th><th class="p-2">λₖ</th></tr></thead>
                            <tbody>`;
                    step.iteration_details.forEach(detail => {
                        html += `<tr class="border-b"><td class="p-2">${detail.k}</td><td class="p-2 font-mono">${formatMatrix(detail.x_k)}</td><td class="p-2 font-mono">${formatMatrix(detail.Ax_k)}</td><td class="p-2 font-mono">${detail.lambda_k.toFixed(6)}</td></tr>`;
                    });
                    html += `</tbody></table></div></details></div>`;
            });
        }
    }

    container.innerHTML = html;
}

export function renderSvdApproximationSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    let html = `<h2 class="result-heading">Kết quả - ${data.method}</h2>`;
    html += `<p class="text-center font-semibold text-lg mb-6 text-green-600">${data.method_used}</p>`;

    // Thông tin tổng quan
    html += `<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6 text-center">
        <div class="p-3 bg-gray-50 rounded-lg">
            <p class="text-sm text-gray-600">Rank gốc</p>
            <p class="text-2xl font-bold text-gray-800">${data.original_rank}</p>
        </div>
        <div class="p-3 bg-blue-50 rounded-lg">
            <p class="text-sm text-gray-600">Rank xấp xỉ</p>
            <p class="text-2xl font-bold text-blue-800">${data.effective_rank}</p>
        </div>
        <div class="p-3 bg-red-50 rounded-lg">
            <p class="text-sm text-gray-600">Sai số tuyệt đối</p>
            <p class="text-2xl font-bold text-red-800">${data.absolute_error.toExponential(4)}</p>
        </div>
        <div class="p-3 bg-green-50 rounded-lg">
            <p class="text-sm text-gray-600">Sai số tương đối</p>
            <p class="text-2xl font-bold text-green-800">${data.relative_error.toFixed(2)}%</p>
        </div>
    </div>`;

    // Hiển thị ma trận
    html += `<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
        <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-2">Ma trận gốc (A)</h3>
            <div class="matrix-display">${formatMatrix(data.original_matrix)}</div>
        </div>
        <div>
            <h3 class="text-lg font-semibold text-gray-700 mb-2">Ma trận xấp xỉ (A')</h3>
            <div class="matrix-display">${formatMatrix(data.approximated_matrix)}</div>
        </div>
    </div>`;
    
    html += `<div class="my-6">
        <h3 class="text-lg font-semibold text-gray-700 mb-2">Ma trận sai số (A - A')</h3>
        <div class="matrix-display">${formatMatrix(data.error_matrix)}</div>
    </div>`;
    
    // Phân tích thành phần
    html += `<h3 class="text-xl font-semibold text-gray-800 my-6 text-center">Phân tích các giá trị kỳ dị</h3>`;
    html += `<p class="text-center text-sm mb-4">Tổng bình phương các giá trị kỳ dị: <strong>${(data.detailed_info.energy_ratio / 100 * (data.retained_components.reduce((a, b) => a + b.singular_value**2, 0) + data.discarded_components.reduce((a, b) => a + b.singular_value**2, 0))).toExponential(4)}</strong>. Phương sai tích luỹ: <strong>${data.detailed_info.energy_ratio.toFixed(2)}%</strong></p>`;

    html += `<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
            <h4 class="text-md font-semibold text-green-700 mb-2">Thành phần được giữ lại (${data.retained_components.length})</h4>
            <div class="overflow-x-auto"><table class="w-full text-sm">
                <thead class="bg-gray-100"><tr><th class="p-2">#</th><th class="p-2">Giá trị kỳ dị (σ)</th><th class="p-2">Phương sai đóng góp (Variance Proportion)</th></tr></thead>
                <tbody>`;
    data.retained_components.forEach(c => {
        html += `<tr class="border-b"><td class="p-2">${c.index}</td><td class="p-2 font-mono">${c.singular_value.toFixed(4)}</td><td class="p-2 font-mono">${c.contribution.toFixed(2)}%</td></tr>`;
    });
    html += `</tbody></table></div>
        </div>
        <div>
            <h4 class="text-md font-semibold text-red-700 mb-2">Thành phần bị loại bỏ (${data.discarded_components.length})</h4>
            <div class="overflow-x-auto"><table class="w-full text-sm">
                <thead class="bg-gray-100"><tr><th class="p-2">#</th><th class="p-2">Giá trị kỳ dị (σ)</th><th class="p-2">Phương sai đóng góp (Variance Proportion)</th></tr></thead>
                <tbody>`;
    if (data.discarded_components.length > 0) {
        data.discarded_components.forEach(c => {
            html += `<tr class="border-b"><td class="p-2">${c.index}</td><td class="p-2 font-mono">${c.singular_value.toFixed(4)}</td><td class="p-2 font-mono">${c.contribution.toFixed(2)}%</td></tr>`;
        });
    } else {
        html += `<tr><td colspan="3" class="p-2 text-center text-gray-500">Không có</td></tr>`;
    }
    html += `</tbody></table></div>
        </div>
    </div>`;

    container.innerHTML = html;
}


/**
 * Hiển thị kết quả của các phương pháp tìm nghiệm (Bisection, Secant, Newton...).
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu kết quả từ API.
 */
export function renderRootFindingSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    let html = `<h2 class="result-heading">Kết quả - ${data.method}</h2>`;
    html += `<p class="text-center font-semibold text-lg mb-6 text-green-600">${data.message}</p>`;

    if (data.extra_info) {
        let extraInfoHtml = '<div class="my-4 p-3 bg-gray-50 rounded-lg text-center text-sm">';
        if (data.extra_info.d !== null && data.extra_info.d !== undefined) {
            extraInfoHtml += `<p>Điểm cố định (Fourier) <strong>d = ${data.extra_info.d.toFixed(6)}</strong>, điểm lặp ban đầu <strong>x₀ = ${data.extra_info.x0.toFixed(6)}</strong>.</p>`;
        } else if (data.extra_info.x0 !== null && data.extra_info.x0 !== undefined) {
            extraInfoHtml += `<p>Điểm lặp ban đầu (Fourier) <strong>x₀ = ${data.extra_info.x0.toFixed(6)}</strong>.</p>`;
        }
        if (data.extra_info.m1 !== null && data.extra_info.m1 !== undefined) {
            const m1_text = `m₁ ≈ <strong>${data.extra_info.m1.toExponential(4)}</strong>`;
            const M1_text = (data.extra_info.M1) ? `, M₁ ≈ <strong>${data.extra_info.M1.toExponential(4)}</strong>` : '';
            const M2_text = (data.extra_info.M2) ? `, M₂ ≈ <strong>${data.extra_info.M2.toExponential(4)}</strong>` : '';
            extraInfoHtml += `<p>${m1_text}${M1_text}${M2_text}</p>`;
        }
        extraInfoHtml += '</div>';
        html += extraInfoHtml;
    }

    html += `
        <div class="my-6 text-center">
            <h3 class="text-lg font-semibold text-gray-700 mb-2">Nghiệm tìm được (x):</h3>
            <p class="text-2xl font-bold font-mono text-blue-700">${data.solution.toFixed(parseInt(document.getElementById('setting-precision')?.value || '7'))}</p>
        </div>`;

    if (data.steps && data.steps.length > 0) {
        const table = data.steps;
        const errorColName = data.error_col_name || "Sai số";

        // <<< SỬA LỖI Ở ĐÂY: Tự động xác định các cột >>>
        const headers = [];
        const firstRowKeys = Object.keys(table[0]);
        
        // Tạo header theo đúng thứ tự mong muốn
        const keyToHeaderMap = {
            'k': 'k', 'n': 'n', 'a': 'a', 'b': 'b', 'c': 'c', 
            'xn': 'x_n', 'fc': 'f(c)', 'fxn': 'f(x_n)', 'dfxn': "f'(x_n)",
            'phixn': 'φ(x_k)', 'abs_diff': '|x_{k+1}-x_k|', 'error': errorColName
        };

        Object.keys(keyToHeaderMap).forEach(key => {
            if (firstRowKeys.includes(key)) {
                headers.push(keyToHeaderMap[key]);
            }
        });
        
        html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-4">Bảng quá trình lặp:</h3>`;
        html += `<div class="overflow-x-auto"><table class="w-full text-sm text-left text-gray-700">`;
        html += `<thead class="text-xs text-gray-800 bg-gray-100"><tr>`;
        headers.forEach(h => html += `<th scope="col" class="px-6 py-3">${h}</th>`);
        html += `</tr></thead><tbody>`;

        const precision = parseInt(document.getElementById('setting-precision')?.value || '7');
        table.forEach(row => {
            html += `<tr class="bg-white border-b">`;
            Object.keys(keyToHeaderMap).forEach(key => {
                if (firstRowKeys.includes(key)) {
                    let value = row[key];
                    let displayValue = 'N/A';
                    if (value !== undefined && value !== null) {
                        if (typeof value === 'number') {
                            if (key === 'k' || key === 'n') {
                                displayValue = value;
                            } else if (Math.abs(value) < 1e-4 && Math.abs(value) > 0) {
                                displayValue = value.toExponential(4);
                            } else {
                                displayValue = value.toFixed(precision);
                            }
                        } else {
                            displayValue = value;
                        }
                    }
                    html += `<td class="px-6 py-4 font-mono">${displayValue}</td>`;
                }
            });
            html += `</tr>`;
        });

        html += `</tbody></table></div>`;
    }
    container.innerHTML = html;
}

/**
 * Hiển thị kết quả giải phương trình đa thức.
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu từ API.
 */
export function renderPolynomialSolution(container, data) {
    let html = `<h2 class="result-heading">Kết quả - Giải phương trình đa thức</h2>`;
    const precision = parseInt(document.getElementById('setting-precision')?.value || '7');

    // Bước 1: Hiển thị đa thức
    html += `<div class="mb-6 text-center"><h3 class="text-lg font-semibold">Đa thức P(x):</h3><div id="poly-str-render" class="text-2xl mt-2"></div></div>`;

    // Bước 2: Hiển thị khoảng chứa nghiệm
    html += `<div class="mb-6 p-3 bg-gray-50 rounded text-center">
        <p class="text-sm"><b>Bước 1: Tìm khoảng chứa nghiệm tổng quát</b></p>
        <p>Tất cả các nghiệm thực (nếu có) của đa thức đều nằm trong khoảng [${data.bounds[0].toFixed(precision)}, ${data.bounds[1].toFixed(precision)}].</p>
    </div>`;

    // Bước 3: Phân ly nghiệm
    html += `<div class="mb-6 p-3 bg-gray-50 rounded text-center">
        <p class="text-sm"><b>Bước 2: Phân ly nghiệm</b></p>
        <p>Các điểm cực trị thực (nghiệm của P'(x)): ${data.critical_points.map(p => p.toFixed(precision)).join(', ') || 'Không có'}</p>
        <p>Các khoảng tìm kiếm nghiệm: ${data.search_intervals.map(inv => `[${inv[0].toFixed(3)}, ${inv[1].toFixed(3)}]`).join('; ')}</p>
    </div>`;

    // Bước 4: Hiển thị các nghiệm tìm được
    html += `<div class="mb-6"><h3 class="text-lg font-semibold text-center">Bước 3: Các nghiệm thực tìm được</h3>`;
    if (data.found_roots.length === 0) {
        html += `<p class="text-center text-gray-600 mt-4">Không tìm thấy nghiệm thực nào trong các khoảng đã xét.</p>`;
    } else {
        data.found_roots.forEach((root, index) => {
            html += `<details class="mt-4 bg-white p-4 rounded-lg shadow border">
                <summary class="cursor-pointer font-semibold text-blue-700">Nghiệm ${index + 1} ≈ ${root.root_value.toFixed(precision)} (tìm thấy trong khoảng [${root.interval[0].toFixed(3)}, ${root.interval[1].toFixed(3)}])</summary>
                <div class="overflow-x-auto mt-4">
                    <p class="text-xs mb-2">Quá trình lặp chia đôi:</p>
                    <table class="w-full text-sm">
                        <thead class="bg-gray-100"><tr>
                            <th class="p-2">k</th><th class="p-2">a</th><th class="p-2">b</th><th class="p-2">c</th><th class="p-2">f(c)</th>
                        </tr></thead>
                        <tbody>`;
            root.bisection_steps.forEach(step => {
                html += `<tr class="border-b">
                    <td class="p-2">${step.k}</td>
                    <td class="p-2 font-mono">${step.a.toFixed(precision)}</td>
                    <td class="p-2 font-mono">${step.b.toFixed(precision)}</td>
                    <td class="p-2 font-mono">${step.c.toFixed(precision)}</td>
                    <td class="p-2 font-mono">${step.fc.toExponential(3)}</td>
                </tr>`;
            });
            html += `</tbody></table></div></details>`;
        });
    }
    html += `</div>`;

    container.innerHTML = html;
    katex.render(data.polynomial_str, document.getElementById('poly-str-render'), { throwOnError: false, displayMode: true });
}

/**
 * Hiển thị kết quả giải hệ phương trình phi tuyến.
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu từ API.
 */
export function renderNonlinearSystemSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');
    
    if (!data || data.error || data.status !== 'success') {
        showError(data ? data.error : 'Đã nhận được phản hồi không hợp lệ từ máy chủ.');
        return;
    }
    
    const precision = parseInt(document.getElementById('setting-precision')?.value || '7');

    let html = `<h2 class="result-heading">Kết quả - ${data.method}</h2>`;
    html += `<p class="text-center font-semibold text-lg mb-6 text-green-600">${data.message}</p>`;

    if (data.method === 'Phương pháp Lặp đơn' && data.convergence_info) {
        const info = data.convergence_info;
        const normSymbol = info.norm_used_for_K === 'infinity' ? '\\infty' : '1';
        
        html += `<div class="my-6 p-4 bg-gray-50 rounded-lg border">
            <h3 class="text-lg font-semibold text-gray-700 mb-2 text-center">Phân tích hội tụ</h3>
            
            <div class="text-center text-sm mb-4 space-y-2">
                <p>Điều kiện hội tụ: <span class="katex-render" data-formula="K = ||J_{\\phi}(X)||_{${normSymbol}} < 1"></span></p>
                ${info.stopping_condition_formula ? `<p>Điều kiện dừng áp dụng: <span class="katex-render" data-formula="${info.stopping_condition_formula}"></span></p>` : ''}
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 items-start">
                <div>
                    <h4 class="text-md font-semibold text-gray-600 mb-2">Ma trận GTLN của đạo hàm riêng <span class="katex-render" data-formula="|J_{\\phi}(X)|"></span>:</h4>
                    <div class="matrix-display">${formatMatrix(info.J_max_vals)}</div>
                </div>
                <div class="text-sm space-y-2">
                    <p>Tổng các hàng (chuẩn vô cùng): <span class="font-mono">${info.max_row_sum.toFixed(4)}</span></p>
                    <p>Tổng các cột (chuẩn 1): <span class="font-mono">${info.max_col_sum.toFixed(4)}</span></p>
                    <p class="mt-2">Sử dụng chuẩn <span class="katex-render" data-formula="${normSymbol}"></span> (giá trị nhỏ hơn).</p>
                    <p class="text-lg font-bold text-blue-700">Hệ số co <span class="katex-render" data-formula="K \\approx ${info.contraction_factor_K.toFixed(6)}"></span></p>
                </div>
            </div>
        </div>`;
    }

    if (data.solution) {
        let solutionHtml = data.solution.map((val, i) => `x<sub>${i+1}</sub> = ${val.toFixed(precision)}`).join('; ');
        html += `
            <div class="my-6 text-center">
                <h3 class="text-lg font-semibold text-gray-700 mb-2">Nghiệm của hệ (X):</h3>
                <p class="text-xl font-bold font-mono text-blue-700">[${solutionHtml}]</p>
            </div>`;
    }

    if (data.jacobian_matrix_latex) {
        html += `<div class="my-6">
            <h3 class="text-lg font-semibold text-gray-700 mb-2 text-center">Ma trận Jacobi J(X):</h3>
            <div class="matrix-display">
                <div class="matrix-container">
                    <table class="matrix-table">`;
        data.jacobian_matrix_latex.forEach(row => {
            html += '<tr>';
            row.forEach(cell => {
                html += `<td><span class="jacobian-cell">${cell}</span></td>`;
            });
            html += '</tr>';
        });
        html += `</table></div></div></div>`;
    }
    
    if (data.J0_inv_matrix) {
        html += `<div class="my-6">
            <h3 class="text-lg font-semibold text-gray-700 mb-2 text-center">Ma trận nghịch đảo J(X₀)⁻¹ (dùng trong suốt quá trình lặp):</h3>
            <div class="matrix-display">${formatMatrix(data.J0_inv_matrix)}</div>
        </div>`;
    }

    if (data.steps && data.steps.length > 0) {
        const table = data.steps;
        const headers = Object.keys(table[0]).sort((a, b) => a === 'k' ? -1 : b === 'k' ? 1 : a.localeCompare(b));

        html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-4">Bảng quá trình lặp:</h3>`;
        html += `<div class="overflow-x-auto"><table class="w-full text-sm text-left text-gray-700">`;
        html += `<thead class="text-xs text-gray-800 bg-gray-100"><tr>`;
        headers.forEach(h => html += `<th scope="col" class="px-6 py-3">${h.replace('error', 'Sai số').replace('relative_error', 'Sai số tương đối')}</th>`);
        html += `</tr></thead><tbody>`;

        table.forEach(row => {
            html += `<tr class="bg-white border-b">`;
            headers.forEach(key => {
                let value = row[key];
                let displayValue = 'N/A';
                if (value !== undefined && value !== null) {
                    if (typeof value === 'number') {
                        if (key === 'k') {
                            displayValue = value;
                        } else if (Math.abs(value) < 1e-4 && Math.abs(value) > 0) {
                            displayValue = value.toExponential(4);
                        } else {
                            displayValue = value.toFixed(precision);
                        }
                    } else {
                        displayValue = value;
                    }
                }
                html += `<td class="px-6 py-4 font-mono">${displayValue}</td>`;
            });
            html += `</tr>`;
        });
        html += `</tbody></table></div>`;
    }

    // Gán nội dung HTML vào container
    container.innerHTML = html;
    
    // === LOGIC RENDER LATEX MỚI, ĐÁNG TIN CẬY HƠN ===
    if (window.katex) {
        // Render tất cả các công thức được đánh dấu bằng class "katex-render"
        container.querySelectorAll('.katex-render').forEach(elem => {
            try {
                katex.render(elem.dataset.formula, elem, {
                    throwOnError: false,
                    displayMode: false
                });
            } catch (e) {
                console.error("Lỗi render Katex:", e);
                elem.textContent = elem.dataset.formula; // Hiển thị mã nguồn nếu lỗi
            }
        });

        // Render các cell trong ma trận Jacobi (giữ nguyên)
        container.querySelectorAll('.jacobian-cell').forEach(elem => {
            try {
                katex.render(elem.textContent, elem, { throwOnError: false, displayMode: false });
            } catch (e) { /* Bỏ qua lỗi render */ }
        });
    }
}

/**
 * Hiển thị kết quả cho Sơ đồ Horner.
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu từ API.
 */
export function renderHornerSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    let html = `<h2 class="result-heading">${data.method}</h2>`;
    const precision = parseInt(document.getElementById('setting-precision')?.value || '4');

    // Biểu diễn đa thức
    html += `<div class="my-6 text-center">
        <p>Cho đa thức <span class="katex-render" data-formula="P(x) = ${data.polynomial_str}"></span> và giá trị <span class="katex-render" data-formula="c = ${data.root}"></span>.</p>
        <p class="mt-2">Ta có: <span class="katex-render" data-formula="${data.result_str_latex}"></span></p>
    </div>`;

    // Bảng Horner
    if (data.division_table) {
        html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-4 text-center">Bảng chia Horner</h3>`;
        html += `<div class="overflow-x-auto flex justify-center">`;
        // Gọi hàm renderHornerDivisionTable đã có
        html += renderHornerDivisionTable(data.division_table, data.root, precision);
        html += `</div>`;
    }
    
    // Kết quả
    html += `<div class="mt-6 p-4 bg-green-50 rounded-lg text-center grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
            <h4 class="font-semibold">Đa thức thương Q(x):</h4>
            <div class="text-lg katex-render" data-formula="Q(x) = ${data.quotient_str}"></div>
        </div>
        <div>
            <h4 class="font-semibold">Giá trị P(${data.root}):</h4>
            <p class="text-lg font-bold text-green-800">${data.value.toFixed(precision)}</p>
        </div>
    </div>`;

    container.innerHTML = html;

    // Render Katex sau khi chèn HTML
    if (window.katex) {
        container.querySelectorAll('.katex-render').forEach(elem => {
            try {
                katex.render(elem.dataset.formula, elem, {
                    throwOnError: false,
                    displayMode: false
                });
            } catch (e) {
                elem.textContent = elem.dataset.formula;
            }
        });
    }
}

export function renderAllDerivativesSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    let html = `<h2 class="result-heading">${data.method}</h2>`;
    const precision = parseInt(document.getElementById('setting-precision')?.value || '4');

    html += `<div class="my-6 text-center">
        <p>Cho đa thức <span class="katex-render" data-formula="P(x) = ${data.polynomial_str}"></span> và giá trị <span class="katex-render" data-formula="c = ${data.root}"></span>.</p>
    </div>`;

    // Bảng kết quả cuối cùng
    html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-4 text-center">Kết quả tính toán</h3>
    <div class="overflow-x-auto flex justify-center mb-6">
        <table class="text-center font-mono border-collapse bg-white shadow rounded-lg">
            <thead class="bg-gray-100">
                <tr>
                    <th class="p-3 border">Đạo hàm</th>
                    <th class="p-3 border">Công thức</th>
                    <th class="p-3 border">Giá trị</th>
                </tr>
            </thead>
            <tbody>`;
    data.derivatives.forEach((derivativeValue, i) => {
        // Lấy hệ số b tương ứng từ data.values
        const b_coefficient = data.values[i]; 
        
        html += `<tr class="border-t">
            <td class="p-3 border"><span class="katex-render" data-formula="P^{(${i})}(${data.root})"></span></td>
            <td class="p-3 border"><span class="katex-render" data-formula="${i}! \\cdot b_{0-${i}}"></span></td>
            <td class="p-3 border font-bold text-blue-700">${derivativeValue.toFixed(precision)}</td>
        </tr>`;
    });
    html += `</tbody></table></div>`;

    // Khai triển Taylor
    html += `<div class="my-6 text-center p-4 bg-green-50 rounded-lg">
        <h4 class="font-semibold">Khai triển Taylor của P(x) tại c = ${data.root}:</h4>
        <div class="text-lg katex-render" data-formula="P(x) = ${data.taylor_str}"></div>
    </div>`;


    // Các bước trung gian
    html += `<h3 class="text-lg font-semibold text-gray-700 mt-8 mb-4 text-center">Các bước Horner mở rộng</h3>`;
    data.steps.forEach(step => {
        html += `<details class="mb-4 bg-white p-3 rounded shadow-sm">
            <summary class="cursor-pointer text-md font-medium text-gray-800 hover:text-blue-600">Bước ${step.step_index + 1}: Chia Q_${step.step_index}(x) cho (x - ${data.root})</summary>
            <div class="mt-3">
                <p class="text-xs mb-2">Đa thức thương: <span class="katex-render" data-formula="Q_{${step.step_index+1}}(x) = ${step.quotient_str}"></span>, Số dư: <span class="font-bold">${step.remainder.toFixed(precision)}</span></p>
                <div class="overflow-x-auto flex justify-center">
                    ${renderHornerDivisionTable(step.division_table, data.root, precision)}
                </div>
            </div>
        </details>`;
    });

    container.innerHTML = html;

    // Render Katex sau khi chèn HTML
    if (window.katex) {
        container.querySelectorAll('.katex-render').forEach(elem => {
            try {
                katex.render(elem.dataset.formula, elem, {
                    throwOnError: false,
                    displayMode: false
                });
            } catch (e) {
                elem.textContent = elem.dataset.formula;
            }
        });
    }
}

/**
 * Hiển thị kết quả cho Sơ đồ Horner nhân.
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu từ API.
 */
export function renderReverseHornerSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    let html = `<h2 class="result-heading">${data.method}</h2>`;
    const precision = parseInt(document.getElementById('setting-precision')?.value || '4');

    // Biểu diễn đa thức
    html += `<div class="my-6 text-center">
        <p>Cho đa thức <span class="katex-render" data-formula="P(x) = ${data.polynomial_str}"></span> và biểu thức <span class="katex-render" data-formula="(x - ${data.root})"></span>.</p>
        <p class="mt-2">Ta có: <span class="katex-render" data-formula="${data.result_str_latex}"></span></p>
    </div>`;

    // Bảng Horner
    if (data.reverse_table) {
        html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-4 text-center">Bảng nhân Horner</h3>`;
        html += `<div class="overflow-x-auto flex justify-center">`;
        html += renderHornerReverseTable(data.reverse_table, data.root, precision);
        html += `</div>`;
    }

    // Kết quả
    html += `<div class="mt-6 p-4 bg-green-50 rounded-lg text-center">
        <div>
            <h4 class="font-semibold">Đa thức tích Q(x):</h4>
            <div class="text-lg katex-render" data-formula="Q(x) = ${data.product_str}"></div>
        </div>
    </div>`;

    container.innerHTML = html;

    // Render Katex sau khi chèn HTML
    if (window.katex) {
        container.querySelectorAll('.katex-render').forEach(elem => {
            try {
                katex.render(elem.dataset.formula, elem, {
                    throwOnError: false,
                    displayMode: false
                });
            } catch (e) {
                elem.textContent = elem.dataset.formula;
            }
        });
    }
}
/** Hiển thị kết quả cho Phép đổi biến trong khai triển Taylor.
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu từ API.
 */
export function renderChangeVariablesSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    let html = `<h2 class="result-heading">${data.method}</h2>`;
    const precision = parseInt(document.getElementById('setting-precision')?.value || '7'); // Tăng độ chính xác

    html += `<div class="my-6 text-center">
        <p>Đa thức gốc: <span class="katex-render" data-formula="P(x) = ${data.original_poly_str}"></span></p>
        <p>Thực hiện phép đổi biến <span class="katex-render-inline" data-formula="t = ${data.a}x + ${data.b}"></span>, suy ra <span class="katex-render-inline" data-formula="x = \\frac{t - (${data.b})}{${data.a}}"></span>.</p>
        <p class="mt-2">Ta sẽ khai triển Taylor cho P(x) tại điểm <span class="katex-render-inline" data-formula="x_0 = -b/a = ${data.root.toFixed(precision)}"></span>.</p>
    </div>`;

    // --- HIỂN THỊ CÁC BƯỚC Bảng chia horner (Giữ nguyên) ---
    html += `<h3 class="text-lg font-semibold text-gray-700 mt-8 mb-4 text-center">Bước 1: Tính các hệ số Taylor dₖ = P⁽ᵏ⁾(x₀)/k! bằng Bảng chia Horner</h3>`;
    data.steps.forEach(step => {
        html += `<details class="mb-4 bg-white p-3 rounded shadow-sm border">
            <summary class="cursor-pointer text-md font-medium text-gray-800 hover:text-blue-600">
                Bước ${step.step_index + 1}: Chia Q_${step.step_index}(x) cho (x - ${data.root.toFixed(precision)}) ⇒ d_${step.step_index} = ${step.remainder_dk.toFixed(precision)}
            </summary>
            <div class="mt-3">
                <p class="text-xs mb-2">Đa thức thương: <span class="katex-render-inline" data-formula="Q_{${step.step_index+1}}(x) = ${step.quotient_str}"></span></p>
                <div class="overflow-x-auto flex justify-center">
                    ${renderHornerDivisionTable(step.division_table, data.root, precision)}
                </div>
            </div>
        </details>`;
    });

    // --- THÊM PHẦN GIẢI THÍCH MỐI LIÊN HỆ ---
    if (data.taylor_explanation) {
        const exp = data.taylor_explanation;
        html += `<h3 class="text-lg font-semibold text-gray-700 mt-8 mb-4 text-center">Bước 2: Xây dựng đa thức Q(t)</h3>`;
        html += `<div class="my-4 p-4 bg-blue-50 rounded-lg border border-blue-200 text-sm">
            <p>Khai triển Taylor của P(x) quanh x₀:</p>
            <div class="text-center my-2 katex-render" data-formula="${exp.taylor_expansion_x_str}"></div>
            <p>Thay <span class="katex-render-inline" data-formula="x - x_0 = t/a"></span> vào khai triển trên:</p>
            <div class="text-center my-2 katex-render" data-formula="${exp.taylor_expansion_t_str}"></div>
            <p class="mt-4 font-semibold">Vậy, các hệ số qₖ của đa thức Q(t) = q₀ + q₁t + ... + qₙtⁿ được tính như sau:</p>
            <ul class="list-disc list-inside mt-2 space-y-1">`;

        exp.q_coeffs_explanation.forEach(q_exp => {
            html += `<li><span class="katex-render-inline" data-formula="${q_exp.formula} \\approx ${q_exp.value.toFixed(precision)}"></span></li>`;
        });

        html += `</ul>
            <p class="mt-3">Sau khi tính toán, ta thu được đa thức Q(t) (sắp xếp theo bậc giảm dần):</p>
        </div>`;
    }

    // Kết quả cuối cùng (Giữ nguyên)
    html += `<div class="mt-6 p-4 bg-green-50 rounded-lg text-center border border-green-200">
        <h4 class="font-semibold">Đa thức theo biến t (Kết quả cuối cùng):</h4>
        <div class="text-lg katex-render" data-formula="Q(t) = ${data.new_poly_str}"></div>
    </div>`;

    container.innerHTML = html;

    // Render Katex sau khi chèn HTML (Giữ nguyên)
    if (window.katex) {
        container.querySelectorAll('.katex-render, .katex-render-inline').forEach(elem => {
            try {
                katex.render(elem.dataset.formula, elem, {
                    throwOnError: false,
                    displayMode: elem.classList.contains('katex-render')
                });
            } catch (e) {
                console.error("Katex render error:", e, "Formula:", elem.dataset.formula);
                elem.textContent = elem.dataset.formula; // Hiển thị mã nguồn nếu lỗi
            }
        });
    }
}

/**
 * Hiển thị kết quả cho Omega function.
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu từ API.
 */
export function renderWFunctionSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    let html = `<h2 class="result-heading">${data.method}</h2>`;
    const precision = parseInt(document.getElementById('setting-precision')?.value || '4');

    // Công thức tổng quát
    html += `<div class="my-6 text-center">
        <p>Tính đa thức: <span class="katex-render" data-formula="${data.w_n_plus_1_latex}"></span>.</p>
    </div>`;
    
    // Kết quả cuối cùng
    html += `<div class="mt-6 p-4 bg-green-50 rounded-lg text-center">
        <h4 class="font-semibold">Đa thức kết quả:</h4>
        <div class="text-lg katex-render" data-formula="w(x) = ${data.final_poly_str}"></div>
    </div>`;

    // Các bước trung gian
    html += `<h3 class="text-lg font-semibold text-gray-700 mt-8 mb-4 text-center">Các bước nhân Horner</h3>`;
    data.steps.forEach(step => {
        html += `<details class="mb-4 bg-white p-3 rounded shadow-sm">
            <summary class="cursor-pointer text-md font-medium text-gray-800 hover:text-blue-600">
                Bước ${step.step_index + 1}: Nhân <span class="katex-render-inline" data-formula="w_{${step.step_index}}(x)"></span> với <span class="katex-render-inline" data-formula="(x - ${step.root})"></span>
            </summary>
            <div class="mt-3">
                <p class="text-xs mb-2">Đa thức hiện tại: <span class="katex-render-inline" data-formula="w_{${step.step_index}}(x) = ${step.w_k_str}"></span></p>
                <p class="text-xs mb-2">Đa thức mới: <span class="katex-render-inline" data-formula="w_{${step.step_index+1}}(x) = ${step.w_k_plus_1_str}"></span></p>
                <div class="overflow-x-auto flex justify-center mt-4">
                    ${renderHornerDivisionTable(step.reverse_table, step.root, precision)}
                </div>
            </div>
        </details>`;
    });

    container.innerHTML = html;

    // Render Katex sau khi chèn HTML
    if (window.katex) {
        container.querySelectorAll('.katex-render, .katex-render-inline').forEach(elem => {
            try {
                katex.render(elem.dataset.formula, elem, {
                    throwOnError: false,
                    displayMode: elem.classList.contains('katex-render')
                });
            } catch (e) {
                elem.textContent = elem.dataset.formula;
            }
        });
    }
}

/**
 * Hiển thị kết quả cho các bài toán Nội suy/Xấp xỉ hàm số.
 * @param {HTMLElement} container - Vùng chứa để hiển thị kết quả.
 * @param {object} data - Dữ liệu từ API.
 */
export function renderInterpolationSolution(container, data) {
    const errorMessageDiv = document.getElementById('error-message');
    if (errorMessageDiv) errorMessageDiv.classList.add('hidden');

    if (!data || data.status !== 'success') {
        showError(data ? data.error : 'Đã nhận được phản hồi không hợp lệ từ máy chủ.');
        return;
    }

    const precision = parseInt(document.getElementById('setting-precision')?.value || '7');

    let html = `<h2 class="result-heading">Kết quả - ${data.method}</h2>`;
    html += `<p class="text-center font-semibold text-lg mb-6 text-green-600">${data.message || ''}</p>`;

    // Hiển thị các mốc nội suy (Chebyshev)
    if (data.nodes) {
        html += `<div class="my-6">
            <h3 class="text-lg font-semibold text-gray-700 mb-2 text-center">Các mốc nội suy:</h3>
            <div class="p-4 bg-gray-50 rounded-lg text-center font-mono text-lg tracking-wider">
                ${data.nodes.map(node => node.toFixed(precision)).join('; &nbsp; ')}
            </div>
        </div>`;
    }
    // Hiển thị các mốc nội suy đã sắp xếp (nếu có)
    if (data.x_nodes_sorted && data.y_nodes_sorted) {
            html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-2 text-center">Các mốc nội suy đã sắp xếp theo thứ tự tăng dần</h3>`;
            html += `<div class="overflow-x-auto mb-4 flex justify-center">`; // Container cho phép cuộn ngang
            html += `<table class="text-sm text-center border border-collapse border-gray-300">`; // Bảng với border
            html += `<thead class="text-xs text-gray-800 bg-gray-100">`;

            // Hàng tiêu đề x_i
            html += `<tr><th class="px-4 py-2 border border-gray-300 font-semibold text-gray-600">xᵢ</th>`;
            data.x_nodes_sorted.forEach(x_val => {
                html += `<td class="px-4 py-2 border border-gray-300 font-mono">${x_val.toFixed(precision)}</td>`;
            });
            html += `</tr>`;

            // Hàng giá trị y_i
            html += `<tr><th class="px-4 py-2 border border-gray-300 font-semibold text-gray-600">yᵢ</th>`;
            data.y_nodes_sorted.forEach(y_val => {
                html += `<td class="px-4 py-2 border border-gray-300 font-mono">${y_val.toFixed(precision)}</td>`;
            });
            html += `</tr>`;

            html += `</thead></table></div>`;
            html += `</div>`;
       }

    // Hiển thị kết quả cho Lagrange
    if (data.method === "Nội suy Lagrange") {
        html += `<div class="my-6 text-center p-4 bg-green-50 rounded-lg">
            <h3 class="font-semibold">Đa thức nội suy Lagrange P(x):</h3>
            <div class="text-lg katex-render" data-formula="P(x) = ${data.polynomial_str}"></div>
        </div>`;

        html += `<details class="mt-6 bg-gray-50 p-3 rounded-lg">
            <summary class="cursor-pointer font-semibold text-gray-700">Xem chi tiết các bước tính toán</summary>
            <div class="mt-4">
                <p class="text-sm">Đa thức <span class="katex-render-inline" data-formula="w(x) = ${data.w_poly_str}"></span></p>
                <div class="mt-4 space-y-4">`;
        
        data.calculation_steps.forEach(step => {
            html += `<div class="p-3 border rounded bg-white">
                <p class="font-semibold text-blue-700">Bước ${step.i + 1}: Tính thành phần cho (x_${step.i}, y_${step.i})</p>
                <ul class="list-disc list-inside text-sm mt-2 space-y-1">
                    <li>Hằng số mẫu: <span class="katex-render-inline" data-formula="D_{${step.i}} = w'(${step.xi}) \\approx ${step.Di_value.toFixed(precision)}"></span></li>
                    <li>Đa thức tử: <span class="katex-render-inline" data-formula="\\frac{w(x)}{x - ${step.xi}} = ${step.w_over_x_minus_xi_str}"></span></li>
                    <li>Thành phần thứ ${step.i+1}: <span class="katex-render-inline" data-formula="\\frac{y_{${step.i}}}{D_{${step.i}}} \\cdot \\frac{w(x)}{x - x_{${step.i}}} = ${step.term_str}"></span></li>
                </ul>
            </div>`;
        });

        html += `</div></div></details>`;
    }
    // Hiển thị kết quả cho Tỷ sai phân 
    if (data.method === "Tỷ sai phân" || data.method === "Nội suy Newton mốc bất kỳ (Tỷ sai phân)") {
        const tableData = data.divided_difference_table;
        if (tableData && tableData.length > 0) {
            const n_rows = tableData.length;
            const n_cols = tableData[0].length;
            html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-4 text-center">Bảng ${data.method}</h3>`;
            html += `<div class="overflow-x-auto"><table class="w-full text-sm text-left text-gray-700">`;

            // Render header
            let headerHtml = `<thead class="text-xs text-gray-800 bg-gray-100"><tr>
                <th class="px-6 py-3">x_i</th>
                <th class="px-6 py-3">y_i</th>`;
            for(let i = 2; i < n_cols; i++) {
                headerHtml += `<th class="px-6 py-3">Cấp ${i-1}</th>`;
            }
            headerHtml += `</tr></thead>`;
            html += headerHtml;

            // Render body
            html += `<tbody>`;
            tableData.forEach((row, rowIndex) => {
                html += `<tr class="bg-white border-b">`;
                row.forEach((cell, colIndex) => {
                    // Xác định điều kiện làm nổi bật
                    const isDiagonal = (colIndex === rowIndex + 1);
                    const isLastRow = (rowIndex === n_rows - 1);
                    // Áp dụng điều kiện từ cột y_i (colIndex = 1) trở đi
                    const highlightClass = (colIndex >= 1 && (isDiagonal || isLastRow)) ? 'font-bold text-red-600' : '';

                    // Chỉ hiển thị giá trị nếu nó nằm trong phần tam giác dưới của bảng
                    if (colIndex <= rowIndex + 1) {
                        html += `<td class="px-6 py-4 font-mono ${highlightClass}">${cell.toFixed(precision)}</td>`;
                    } else {
                        html += `<td class="px-6 py-4 font-mono"></td>`; // Ô trống
                    }
                });
                html += `</tr>`;
            });
            html += `</tbody></table></div>`;
        }
    }
    if (data.method === "Sai phân") {
        const tableData = data.finite_difference_table;
        if (tableData && tableData.length > 0) {
            const n_rows = tableData.length;
            const n_cols = tableData[0].length;
            html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-4 text-center">Bảng ${data.method}</h3>`;
            html += `<div class="overflow-x-auto"><table class="w-full text-sm text-left text-gray-700">`;

            // Render header
            let headerHtml = `<thead class="text-xs text-gray-800 bg-gray-100"><tr>
                <th class="px-6 py-3">x_i</th>
                <th class="px-6 py-3">y_i</th>`;
            for(let i = 2; i < n_cols; i++) {
                headerHtml += `<th class="px-6 py-3">Cấp ${i-1}</th>`;
            }
            headerHtml += `</tr></thead>`;
            html += headerHtml;

            // Render body
            html += `<tbody>`;
            tableData.forEach((row, rowIndex) => {
                html += `<tr class="bg-white border-b">`;
                row.forEach((cell, colIndex) => {
                    // Xác định điều kiện làm nổi bật
                    const isDiagonal = (colIndex === rowIndex + 1);
                    const isLastRow = (rowIndex === n_rows - 1);
                    // Áp dụng điều kiện từ cột y_i (colIndex = 1) trở đi
                    const highlightClass = (colIndex >= 1 && (isDiagonal || isLastRow)) ? 'font-bold text-red-600' : '';

                    // Chỉ hiển thị giá trị nếu nó nằm trong phần tam giác dưới của bảng
                    if (colIndex <= rowIndex + 1) {
                        html += `<td class="px-6 py-4 font-mono ${highlightClass}">${cell.toFixed(precision)}</td>`;
                    } else {
                        html += `<td class="px-6 py-4 font-mono"></td>`; // Ô trống
                    }
                });
                html += `</tr>`;
            });
            html += `</tbody></table></div>`;
        }
    }

    if (data.method === "Nội suy Newton mốc cách đều" || data.method === "Nội suy Newton mốc bất kỳ (Tỷ sai phân)") {

        // Hiển thị bảng Sai phân (chỉ cho mốc cách đều)
        if (data.method === "Nội suy Newton mốc cách đều") {
            html += `<div class="my-6">
                <h3 class="text-lg font-semibold text-gray-700 mb-2 text-center">Bảng sai phân (h = ${data.h.toFixed(precision)})</h3>`;
            // ... (code render bảng sai phân như cũ) ...
             const tableDataFD = data.finite_difference_table;
            if (tableDataFD && tableDataFD.length > 0) {
                const n_rowsFD = tableDataFD.length;
                const n_colsFD = tableDataFD[0].length;
                html += `<div class="overflow-x-auto"><table class="w-full text-sm text-left text-gray-700">`;
                let headerHtmlFD = `<thead class="text-xs text-gray-800 bg-gray-100"><tr>
                    <th class="px-6 py-3">x_i</th>
                    <th class="px-6 py-3">y_i</th>`;
                for(let i = 2; i < n_colsFD; i++) {
                    headerHtmlFD += `<th class="px-6 py-3 katex-render-inline" data-formula="\\Delta^{${i-1}}y"></th>`;
                }
                headerHtmlFD += `</tr></thead>`;
                html += headerHtmlFD;
                html += `<tbody>`;
                tableDataFD.forEach((row, rowIndex) => {
                    html += `<tr class="bg-white border-b">`;
                    row.forEach((cell, colIndex) => {
                        const isForwardDiagonal = (colIndex === rowIndex + 1);
                        const isBackwardLastRow = (rowIndex === n_rowsFD - 1);
                        let highlightClass = '';
                        if (colIndex > 0 && (isForwardDiagonal || isBackwardLastRow)) {
                            highlightClass = 'font-bold text-red-600';
                        }
                        if (colIndex <= rowIndex + 1) {
                            html += `<td class="px-6 py-4 font-mono ${highlightClass.trim()}">${cell.toFixed(precision)}</td>`;
                        } else {
                            html += `<td class="px-6 py-4 font-mono"></td>`;
                        }
                    });
                    html += `</tr>`;
                });
                html += `</tbody></table></div>`;
            }
            html += `</div>`;
        }

        // Hàm render chi tiết (cập nhật để dùng chung)
        const renderDetailsNewton = (title, details, isForward, isEquidistant, h=null) => {
            const variable = isEquidistant ? 't' : 'x';
            const poly_str = isEquidistant ? details.polynomial_str_t : details.polynomial_str_x;
            const final_poly_str = details.polynomial_str_x;
            const diff_label = isEquidistant ? (isForward ? '\\Delta' : '\\nabla') : 'f';
            const diff_symbol = isEquidistant ? (isForward ? 'y_0' : 'y_n') : `[x_0${isForward ? "" : ",...,x_n"}]`; // Đơn giản hóa

            let formula = `P_n(${variable}) = `;
            if (isEquidistant) {
                formula += isForward
                    ? `y_0 + \\sum_{i=1}^{n} \\frac{${diff_label}^i ${diff_symbol}}{i!} t(t-1)...(t-i+1)`
                    : `y_n + \\sum_{i=1}^{n} \\frac{${diff_label}^i ${diff_symbol}}{i!} t(t+1)...(t+i-1)`;
            } else {
                    if (isForward) {
                        // Công thức Newton Tiến mốc bất kỳ (đúng)
                        formula += `f[x_0] + \\sum_{i=1}^{n} f[x_0,...,x_i] (x-x_0)...(x-x_{i-1})`;
                    } else {
                        // Công thức Newton Lùi mốc bất kỳ
                        formula += `f[x_n] + \\sum_{i=1}^{n} f[x_{n-i},...,x_n] (x-x_n)(x-x_{n-1})...(x-x_{n-i+1})`;
                    }
            }

            let w_polynomials = isEquidistant ? details.w_polynomials_t : details.w_polynomials_x;
            let coeffs_scaled_or_diffs = isEquidistant ? details.coeffs_scaled : details.diffs;

            let w_table_html = `<div class="overflow-x-auto my-4">
                <table class="w-full text-sm text-center">
                    <thead class="bg-gray-200 text-xs text-gray-700">
                        <tr>
                            <th class="p-2">i</th>
                            <th class="p-2">Hệ số (${isEquidistant ? `${diff_label}^iy / i!` : 'Tỷ sai phân'})</th>
                            <th class="p-2">Đa thức cơ sở wᵢ(${variable})</th>
                        </tr>
                    </thead>
                    <tbody>`;
            w_polynomials.forEach((w_poly, i) => {
                w_table_html += `<tr class="border-b bg-white">
                    <td class="p-2 font-mono">${i}</td>
                    <td class="p-2 font-mono">${coeffs_scaled_or_diffs[i].toFixed(precision)}</td>
                    <td class="p-2 text-left katex-render-inline" data-formula="${format_poly_str_js(w_poly, variable)}"></td>
                </tr>`;
            });
            w_table_html += `</tbody></table></div>`;

            let resultHtml = `
            <div class="mt-8">
                <h3 class="text-xl font-semibold text-gray-800 text-center mb-4">${title}</h3>
                <div class="p-4 bg-gray-50 rounded-lg border space-y-4">
                    <p class="text-sm">Bắt đầu từ mốc <span class="katex-render-inline" data-formula="x_{${isForward ? '0' : 'n'}} = ${details.start_node}"></span>, áp dụng công thức:</p>
                    <div class="text-center text-lg katex-render" data-formula="${formula}"></div>
                    <p class="text-sm font-semibold">1. Xây dựng các đa thức cơ sở wᵢ(${variable}) và hệ số:</p>
                    ${w_table_html}`;

            if (isEquidistant) {
               resultHtml += `<p class="text-sm font-semibold">2. Đa thức theo biến t:</p>
                    <div class="text-center text-lg katex-render" data-formula="P_n(t) = ${poly_str}"></div>
                    <p class="text-sm mt-2 font-semibold">3. Đổi biến <span class="katex-render-inline" data-formula="x = ${details.start_node} + t \\cdot ${h.toFixed(precision)}"></span> để có đa thức cuối cùng:</p>`;
            } else {
                 resultHtml += `<p class="text-sm font-semibold">2. Tổng hợp đa thức P(x):</p>
                 <p class="text-xs text-center">(Cộng các tích [Hệ số * Đa thức cơ sở])</p>`;
            }
            resultHtml += `<div class="text-lg text-center p-3 bg-green-50 rounded-md katex-render" data-formula="P_n(x) = ${final_poly_str}"></div>
                </div>
            </div>`;
            return resultHtml;
        };

        // Gọi hàm render chi tiết cho cả hai trường hợp
        html += renderDetailsNewton("Chi tiết quá trình tính Newton Tiến", data.forward_interpolation, true, data.method === "Nội suy Newton mốc cách đều", data.h);
        html += renderDetailsNewton("Chi tiết quá trình tính Newton Lùi", data.backward_interpolation, false, data.method === "Nội suy Newton mốc cách đều", data.h);
    }

    if (data.method === "Nội suy trung tâm Gauss I") {
        html += `<div class="my-6 text-center p-4 bg-green-50 rounded-lg border border-green-200">
            <h3 class="font-semibold">Đa thức nội suy Gauss I P(x):</h3>
            <div class="text-lg katex-render" data-formula="P(x) = ${data.polynomial_str_x}"></div>
        </div>`;

        // Bảng sai phân hữu hạn
         if (data.finite_difference_table && data.finite_difference_table.length > 0) {
            html += `<h3 class="text-lg font-semibold text-gray-700 mt-6 mb-2 text-center">Bảng sai phân hữu hạn (h = ${data.h.toFixed(precision)})</h3>`;
            const tableDataFD = data.finite_difference_table;
            const n_rowsFD = tableDataFD.length;
            const start_row_index = Math.floor((n_rowsFD - 1) / 2);

            html += `<div class="overflow-x-auto"><table class="w-full text-sm text-left text-gray-700">`;
            let headerHtmlFD = `<thead class="text-xs text-gray-800 bg-gray-100"><tr>
                <th class="px-6 py-3">x_i</th>
                <th class="px-6 py-3">y_i</th>`;
            for (let i = 1; i < n_rowsFD; i++) {
                headerHtmlFD += `<th class="px-6 py-3 katex-render-inline" data-formula="\\Delta^{${i}}y"></th>`;
            }
            headerHtmlFD += `</tr></thead>`;
            html += headerHtmlFD;
            html += `<tbody>`;

            tableDataFD.forEach((row, rowIndex) => {
                html += `<tr class="bg-white border-b">`;
                row.forEach((cell, colIndex) => {
                    let highlightClass = '';
                    if (colIndex > 0) {
                         const central_diff_index_in_list = colIndex - 1;
                         if (central_diff_index_in_list >= 0 && central_diff_index_in_list < data.central_finite_diffs.length) {
                             const expected_row_for_diff = start_row_index + Math.floor((central_diff_index_in_list + 1) / 2);
                              if (rowIndex === expected_row_for_diff && colIndex <= rowIndex + 1) {
                                  highlightClass = 'font-bold text-red-600';
                              }
                         }
                    }
                    if (colIndex <= rowIndex + 1) {
                        html += `<td class="px-6 py-4 font-mono ${highlightClass.trim()}">${cell.toFixed(precision)}</td>`;
                    } else {
                        html += `<td class="px-6 py-4 font-mono"></td>`;
                    }
                });
                html += `</tr>`;
            });
            html += `</tbody></table></div>`;
        }


        // Chi tiết tính toán
        html += `<details class="mt-6 bg-gray-50 p-3 rounded-lg border">
            <summary class="cursor-pointer font-semibold text-gray-700">Xem chi tiết các bước tính toán Gauss I</summary>
            <div class="mt-4 space-y-4 text-sm">
                 <p>Mốc trung tâm: <span class="katex-render-inline" data-formula="x_0 = ${data.start_node.toFixed(precision)}"></span>, Bước nhảy: <span class="katex-render-inline" data-formula="h = ${data.h.toFixed(precision)}"></span>.</p>
                <p>Công thức Gauss I (theo biến <span class="katex-render-inline" data-formula="t = (x-x_0)/h"></span>):</p>
                <div class="text-center text-lg katex-render" data-formula="P_n(t) = y_0 + t \\Delta y_0 + \\frac{t(t-1)}{2!} \\Delta^2 y_{-1} + \\frac{t(t-1)(t+1)}{3!} \\Delta^3 y_{-1} + \\dots"></div>

                <p class="font-semibold mt-4">1. Các sai phân trung tâm <span class="katex-render-inline" data-formula="\\Delta^i y_{k}"></span> được sử dụng:</p>
                <div class="p-2 bg-white rounded border flex flex-wrap gap-x-4 gap-y-2 justify-center">`;
        data.central_finite_diffs.forEach((diff, i) => {
             let symbol = '';
             let subscript_index = 0;
             if (i === 0) { symbol = `y`; }
             else {
                 symbol = `\\Delta^{${i}}y`;
                 subscript_index = Math.floor((1 - i) / 2);
             }
             const subscript = `_{${subscript_index}}`;
             html += `<span class="katex-render-inline" data-formula="${symbol}${subscript} \\approx ${diff.toFixed(precision)}"></span>`;
        });
        html += `</div>

                <p class="font-semibold mt-4">2. Tính các hệ số <span class="katex-render-inline" data-formula="a_i = \\frac{\\Delta^i y_k}{i! h^i}"></span>:</p> 
                    <table class="w-full text-sm text-center">
                        <thead class="bg-gray-200 text-xs text-gray-700">
                            <tr>
                                <th class="p-2">i</th>
                                <th class="p-2">Sai phân sử dụng</th>
                                <th class="p-2">Công thức aᵢ</th>
                                <th class="p-2">Giá trị aᵢ</th>
                            </tr>
                        </thead>
                        <tbody>`;
            data.c_coeffs.forEach((c_coeff, i) => { // <<< Dùng c_coeffs (đã chia h^i)
                 let symbol = '';
                 let subscript_index = 0;
                 if (i === 0) { symbol = `y`; }
                 else {
                     symbol = `\\Delta^{${i}}y`;
                     subscript_index = Math.floor((1-i)/2);
                 }
                  const subscript = `_{${subscript_index}}`;
                 const diff_symbol_latex = `${symbol}${subscript}`;
                 // Hiển thị công thức đầy đủ
                 const formula_latex = `a_{${i}} = \\frac{${diff_symbol_latex}}{${i}! h^{${i}}}`;

                html += `<tr class="border-b bg-white">
                            <td class="p-2 font-mono">${i}</td>
                            <td class="p-2 katex-render-inline" data-formula="${diff_symbol_latex} \\approx ${data.central_finite_diffs[i].toFixed(precision)}"></td>
                            <td class="p-2 katex-render-inline" data-formula="${formula_latex}"></td> 
                            <td class="p-2 font-mono">${c_coeff.toFixed(precision)}</td>
                         </tr>`;
            });
            html += `</tbody></table></div>

                <p class="font-semibold mt-4">3. Xây dựng các đa thức cơ sở <span class="katex-render-inline" data-formula="w_i(t)"></span>:</p>
                 <div class="overflow-x-auto my-2">
                    <table class="w-full text-sm text-center">
                        <thead class="bg-gray-200 text-xs text-gray-700">
                            <tr>
                                <th class="p-2">i</th>
                                <th class="p-2">t_i</th>
                                <th class="p-2">Hệ số wᵢ(t)</th>
                            </tr>
                        </thead>
                        <tbody>`;
            const n_nodes = data.finite_difference_table.length;
            for(let i = 0; i < data.w_table_coeffs.length; i++) {
                 const w_poly_str_coeffs = format_poly_str_js(data.w_table_coeffs[i], 't');
                
                 html += `<tr class="border-b bg-white">
                            <td class="p-2 font-mono">${i}</td>
                            <td class="p-2 text-left katex-render-inline" data-formula="${w_poly_str_coeffs}"></td>
                          </tr>`;
            }
            html += `</tbody></table></div>

                <p class="font-semibold mt-4">4. Tổng hợp đa thức <span class="katex-render-inline" data-formula="P(t) = \\sum a_i w_i(t)"></span>:</p>
                 <div class="text-center text-lg p-2 bg-yellow-50 rounded katex-render" data-formula="P(t) = ${data.polynomial_str_t}"></div>

                <p class="font-semibold mt-4">5. Đổi biến <span class="katex-render-inline" data-formula="x = x_0 + th = ${data.start_node.toFixed(precision)} + t \\cdot ${data.h.toFixed(precision)}"></span> để được đa thức cuối cùng P(x):</p>
                <div class="text-center text-lg p-3 bg-green-100 rounded border border-green-300 katex-render" data-formula="P(x) = ${data.polynomial_str_x}"></div>

            </div>
        </details>`;
    }

    container.innerHTML = html;
    
    // Render Katex sau khi chèn HTML
    if (window.katex) {
        container.querySelectorAll('.katex-render, .katex-render-inline').forEach(elem => {
            try {
                katex.render(elem.dataset.formula, elem, {
                    throwOnError: false,
                    displayMode: elem.classList.contains('katex-render')
                });
            } catch (e) {
                elem.textContent = elem.dataset.formula;
            }
        });
    }
}

