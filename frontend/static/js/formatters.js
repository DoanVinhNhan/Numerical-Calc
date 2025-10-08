// frontend/static/js/formatters.js

/**
 * Chuyển đổi một mảng 2D (ma trận) thành một bảng HTML.
 * @param {number[][]} matrix - Ma trận cần định dạng.
 * @param {string} [label=''] - Nhãn tùy chọn (ví dụ: 'A', 'X').
 * @returns {string} - Chuỗi HTML của bảng.
 */
export function formatMatrix(matrix, label = '') {
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
        row.forEach(cell => {
            const num = Number(cell);
            // Hiển thị số nguyên nếu không có phần thập phân sau khi làm tròn
            const formattedCell = Math.abs(num - Math.round(num)) < 1e-9 ? Math.round(num) : num.toFixed(precision);
            html += `<td>${formattedCell}</td>`;
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
        const num_null_vectors = null_space_vectors[0].length; // Số vector cơ sở (k)
        const num_solution_cols = particular_solution[0].length; // Số cột của nghiệm (m)

        // Lặp qua từng vector cơ sở v_i của không gian null
        for (let i = 0; i < num_null_vectors; i++) {
            // Trích xuất vector v_i (kích thước n x 1)
            const vector_vi = null_space_vectors.map(row => [row[i]]);
            
            html += `<span class="font-bold text-2xl mx-2">+</span>`;
            
            // Hiển thị ma trận V (trong trường hợp này là vector v_i)
            html += formatMatrix(vector_vi);
            
            // Dấu nhân ma trận
            html += `<span class="font-bold text-lg mx-1"> </span>`;

            // Tạo ma trận tham số C (kích thước 1 x m)
            let param_matrix_html = '<div class="matrix-container">';
            param_matrix_html += '<table class="matrix-table"><tr>';
            for (let j = 0; j < num_solution_cols; j++) {
                // Ký hiệu tham số là t_{i,j}
                param_matrix_html += `<td>t<sub>${i + 1},${j + 1}</sub></td>`;
            }
            param_matrix_html += '</tr></table></div>';
            
            // Hiển thị ma trận tham số C
            html += param_matrix_html;
        }
    }
    
    html += '</div>';
    return html;
}