// frontend/static/js/api.js

const API_BASE_URL = '/api';

/**
 * Gửi yêu cầu giải hệ phương trình tuyến tính đến backend.
 * @param {string} method - Tên phương pháp (ví dụ: 'gauss', 'gauss-jordan').
 * @param {string} matrixA - Chuỗi biểu diễn ma trận A.
 * @param {string} matrixB - Chuỗi biểu diễn vector b.
 * @param {string} zeroTolerance - Ngưỡng làm tròn về 0.
 * @returns {Promise<object>} - Dữ liệu JSON trả về từ API.
 */
export async function solveLinearSystem(method, matrixA, matrixB, zeroTolerance) {
    const response = await fetch(`${API_BASE_URL}/linear-algebra/solve/${method}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            matrix_a: matrixA, 
            matrix_b: matrixB,
            zero_tolerance: zeroTolerance
        }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định từ máy chủ.');
    }
    
    return response.json();
}