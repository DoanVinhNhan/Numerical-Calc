// frontend/static/js/formatters.js

/**
 * Chuyển đổi một mảng 2D (ma trận) thành một bảng HTML.
 * @param {number[][]} matrix - Ma trận cần định dạng.
 * @param {string} [label=''] - Nhãn tùy chọn (ví dụ: 'A', 'X').
 * @returns {string} - Chuỗi HTML của bảng.
 */
export function formatMatrix(matrix, label = '', num_vars = -1) {
    if (!matrix || matrix.length === 0) {
        return '<p>Không có dữ liệu ma trận.</p>';
    }

    const precision = parseInt(document.getElementById('setting-precision')?.value || '4');
    
    let html = '';
    if (label) {
        html += `<span class="font-bold text-lg mr-2">${label} = </span>`;
    }
    
    html += '<div class="matrix-container">';
    html += '<table class="matrix-table">';
    matrix.forEach(row => {
        html += '<tr>';
        row.forEach((cell, colIndex) => { // Thêm colIndex vào đây
            const num = Number(cell);
            const formattedCell = Math.abs(num - Math.round(num)) < 1e-9 ? Math.round(num) : num.toFixed(precision);
            
            // Nếu đây là cột đầu tiên của phần B, thêm lớp CSS
            const separatorClass = (num_vars > 0 && colIndex === num_vars) ? 'class="augmented-separator"' : '';
            
            html += `<td ${separatorClass}>${formattedCell}</td>`;
        });
        html += '</tr>';
    });
    html += '</table>';
    html += '</div>';

    return html;
}

/**
 * Định dạng nghiệm tổng quát cho trường hợp vô số nghiệm.
 * @param {object} generalSolution - Đối tượng chứa nghiệm riêng và các vector null space.
 * @returns {string} - Chuỗi HTML biểu diễn nghiệm tổng quát.
 */
export function formatGeneralSolution(generalSolution) {
    const { particular_solution, null_space_vectors } = generalSolution;
    
    let html = '<div class="flex items-center justify-center flex-wrap gap-x-2">';

    // 1. Bắt đầu với "X ="
    html += '<span class="font-bold text-lg mr-2">X = </span>';

    // 2. Hiển thị ma trận nghiệm riêng Xp
    html += formatMatrix(particular_solution);

    // 3. Hiển thị phần không gian null (V * C)
    if (null_space_vectors && null_space_vectors.length > 0) {
        html += `<span class="font-bold text-2xl mx-2">+</span>`;

        // 3a. Hiển thị ma trận V (gộp các vector không gian null)
        // Backend đã trả về null_space_vectors dưới dạng một ma trận n x k
        html += formatMatrix(null_space_vectors);

        // Dấu nhân ma trận
        html += `<span class="font-bold text-lg mx-1">*</span>`;

        // 3b. Xây dựng ma trận tham số C (k x m)
        const num_null_vectors = null_space_vectors[0].length; // Số cột của V (k)
        const num_solution_cols = particular_solution[0].length; // Số cột của Xp (m)

        let param_matrix_html = '<div class="matrix-container">';
        param_matrix_html += '<table class="matrix-table">';
        // Lặp k lần để tạo k hàng
        for (let i = 0; i < num_null_vectors; i++) {
            param_matrix_html += '<tr>';
            // Lặp m lần để tạo m cột
            for (let j = 0; j < num_solution_cols; j++) {
                param_matrix_html += `<td>t<sub>${i + 1},${j + 1}</sub></td>`;
            }
            param_matrix_html += '</tr>';
        }
        param_matrix_html += '</table></div>';
        
        // Hiển thị ma trận tham số C
        html += param_matrix_html;
    }
    
    html += '</div>';
    return html;
}