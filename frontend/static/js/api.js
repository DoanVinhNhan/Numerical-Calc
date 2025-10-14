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

export async function solveSimpleIterationSystem(matrixB, matrixD, x0, tolerance, maxIter, normChoice) {
    const response = await fetch(`${API_BASE_URL}/linear-algebra/solve/simple-iteration`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            matrix_b: matrixB, // Gửi B
            matrix_d: matrixD, // Gửi d
            x0: x0,
            tolerance: tolerance,
            max_iter: maxIter,
            norm_choice: normChoice
        }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định từ máy chủ.');
    }
    
    return response.json();
}

export async function calculateInverseIterative(method, matrixA, tolerance, maxIter, x0Method) {
    const response = await fetch(`${API_BASE_URL}/linear-algebra/inverse/${method}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            matrix_a: matrixA,
            tolerance: tolerance,
            max_iter: maxIter,
            x0_method: x0Method
        }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

export async function calculateEigen(method, payload) {
    const endpoint = method === 'svd' ? 'svd' : `eigen/${method}`;
    const response = await fetch(`${API_BASE_URL}/linear-algebra/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

/**
 * Gửi yêu cầu tính toán ma trận xấp xỉ SVD.
 * @param {string} matrixA - Chuỗi ma trận A.
 * @param {string} method - Phương pháp xấp xỉ ('rank-k', 'threshold', 'error-bound').
 * @param {number} value - Giá trị tương ứng với phương pháp (k, ngưỡng, hoặc giới hạn sai số).
 * @returns {Promise<object>} - Dữ liệu JSON trả về từ API.
 */
export async function calculateSvdApproximation(matrixA, method, value) {
    const response = await fetch(`${API_BASE_URL}/linear-algebra/svd-approximation`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            matrix_a: matrixA,
            method: method,
            value: value
        }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định từ máy chủ.');
    }

    return response.json();
}


/**
 * Gửi yêu cầu giải phương trình f(x)=0 đến backend.
 * @param {object} payload - Dữ liệu yêu cầu bao gồm method, expression, a, b, ...
 * @returns {Promise<object>} - Dữ liệu JSON trả về từ API.
 */
export async function solveNonlinearEquation(payload) {
    const response = await fetch(`${API_BASE_URL}/root-finding/solve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}