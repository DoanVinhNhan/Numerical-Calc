// frontend/static/js/formatters.js

/**
 * Hàm nội bộ: Chuyển đổi một số (thực hoặc phức) thành chuỗi hiển thị.
 */
export function formatCell(cell, precision) {
    // Xử lý trường hợp số phức dạng object {real, imag}
    if (typeof cell === 'object' && cell !== null && 'real' in cell && 'imag' in cell) {
        if (Math.abs(cell.imag) < 1e-9) return cell.real.toFixed(precision);
        const imagSign = cell.imag >= 0 ? '+' : '-';
        return `${cell.real.toFixed(precision)} ${imagSign} ${Math.abs(cell.imag).toFixed(precision)}i`;
    }
    // Xử lý trường hợp số thông thường
    const number = Number(cell);
    if (isNaN(number)) return 'N/A'; // Hoặc một giá trị mặc định khác
    return number.toFixed(precision);
}

/**
 * Chuyển đổi một mảng 2D (ma trận) thành một bảng HTML.
 * Có khả năng hiển thị số phức.
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
        if (Array.isArray(row)) {
            row.forEach((cell, colIndex) => {
                const separatorClass = (num_vars > 0 && colIndex === num_vars) ? 'class="augmented-separator"' : '';
                html += `<td ${separatorClass}>${formatCell(cell, precision)}</td>`;
            });
        }
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

// Hàm trợ giúp để render bảng Horner (có thể tách ra nếu muốn)
export function renderHornerDivisionTable(table, root, precision) {
    const n = table[0].length;
    let tableHtml = `<table class="text-center font-mono border-collapse text-sm">
            <tbody>
                <tr class="border-b-2 border-gray-700">
                    <td class="p-2 border-r-2 border-gray-700">a_i</td>`;
    for (let i = 0; i < n; i++) {
        tableHtml += `<td class="p-2">${table[0][i].toFixed(precision)}</td>`;
    }
    tableHtml += `</tr>
                <tr class="border-b-2 border-gray-700">
                    <td class="p-2 border-r-2 border-gray-700">c=${root}</td>`;
    for (let i = 0; i < n; i++) {
        tableHtml += `<td class="p-2">${table[1][i].toFixed(precision)}</td>`;
    }
    tableHtml += `</tr>
                <tr>
                    <td class="p-2 border-r-2 border-gray-700">b_i</td>`;
    for (let i = 0; i < n; i++) {
        tableHtml += `<td class="p-2 font-bold text-blue-700">${table[2][i].toFixed(precision)}</td>`;
    }
    tableHtml += `</tr>
            </tbody>
        </table>`;
    return tableHtml;
}

export function renderHornerReverseTable(table, root, precision) {
    const n = table[0].length;
    let tableHtml = `<table class="text-center font-mono border-collapse text-sm">
            <tbody>
                <tr class="border-b-2 border-gray-700">
                    <td class="p-2 border-r-2 border-gray-700">b_i</td>`;
    for (let i = 0; i < n; i++) {
        tableHtml += `<td class="p-2">${table[0][i].toFixed(precision)}</td>`;
    }
    tableHtml += `</tr>
                <tr class="border-b-2 border-gray-700">
                    <td class="p-2 border-r-2 border-gray-700">c=${root}</td>`;
    for (let i = 0; i < n; i++) {
        tableHtml += `<td class="p-2">${table[1][i].toFixed(precision)}</td>`;
    }
    tableHtml += `</tr>
                <tr>
                    <td class="p-2 border-r-2 border-gray-700">a_i</td>`;
    for (let i = 0; i < n; i++) {
        tableHtml += `<td class="p-2 font-bold text-blue-700">${table[2][i].toFixed(precision)}</td>`;
    }
    tableHtml += `</tr>
            </tbody>
        </table>`;
    return tableHtml;
}