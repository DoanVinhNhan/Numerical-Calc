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

/**
 * Gửi yêu cầu tính ma trận nghịch đảo đến backend.
 * @param {string} method - Tên phương pháp (ví dụ: 'gauss-jordan').
 * @param {string} matrixA - Chuỗi biểu diễn ma trận A.
 * @param {string} zeroTolerance - Ngưỡng làm tròn về 0.
 * @returns {Promise<object>} - Dữ liệu JSON trả về từ API.
 */
export async function calculateInverse(method, matrixA, zeroTolerance) {
    const response = await fetch(`${API_BASE_URL}/linear-algebra/inverse/${method}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            matrix_a: matrixA,
            zero_tolerance: zeroTolerance
        }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định từ máy chủ.');
    }
    
    return response.json();
}

/**
 * Gửi yêu cầu giải hệ phương trình tuyến tính bằng phương pháp lặp.
 * @param {string} method - Tên phương pháp ('jacobi', 'gauss-seidel').
 * @param {string} matrixA - Chuỗi ma trận A.
 * @param {string} matrixB - Chuỗi vector b.
 * @param {string} x0 - Chuỗi vector lặp ban đầu X₀.
 * @param {string} tolerance - Sai số cho phép.
 * @param {string} maxIter - Số lần lặp tối đa.
 * @returns {Promise<object>} - Dữ liệu JSON trả về từ API.
 */
export async function solveIterativeLinearSystem(method, matrixA, matrixB, x0, tolerance, maxIter) {
    const response = await fetch(`${API_BASE_URL}/linear-algebra/solve/${method}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            matrix_a: matrixA, 
            matrix_b: matrixB,
            x0: x0,
            tolerance: tolerance,
            max_iter: maxIter
        }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định từ máy chủ.');
    }
    
    return response.json();
}