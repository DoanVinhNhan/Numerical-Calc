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
/**
 * Gửi yêu cầu giải phương trình đa thức đến backend.
 * @param {string} coeffs - Chuỗi các hệ số, cách nhau bằng dấu cách.
 * @param {string} tolerance - Sai số cho phép.
 * @param {string} maxIter - Số lần lặp tối đa.
 * @returns {Promise<object>}
 */
export async function solvePolynomial(coeffs, tolerance, maxIter) {
    const response = await fetch(`${API_BASE_URL}/polynomial/solve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ coeffs, tolerance, max_iter: maxIter }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

/**
 * Gửi yêu cầu giải hệ phương trình phi tuyến đến backend.
 * @param {object} payload - Dữ liệu yêu cầu.
 * @returns {Promise<object>}
 */
export async function solveNonlinearSystem(payload) {
    const response = await fetch(`${API_BASE_URL}/nonlinear-systems/solve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định từ máy chủ.');
    }
    return response.json();
}

/**
 * Lấy các mốc nội suy tối ưu Chebyshev từ backend.
 * @param {string} a - Điểm đầu khoảng.
 * @param {string} b - Điểm cuối khoảng.
 * @param {string} n - Số mốc nội suy.
 * @returns {Promise<object>}
 */
export async function getChebyshevNodes(a, b, n) {
    const response = await fetch(`${API_BASE_URL}/interpolation/chebyshev-nodes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ a, b, n }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

/**
 * Gửi yêu cầu tính toán bằng Sơ đồ Horner.
 * @param {string} coeffs - Chuỗi các hệ số của đa thức.
 * @param {string} root - Giá trị c để chia cho (x-c).
 * @returns {Promise<object>}
 */
export async function calculateSyntheticDivision(coeffs, root) {
    const response = await fetch(`${API_BASE_URL}/horner/synthetic-division`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ coeffs, root }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}
export async function calculateAllDerivatives(coeffs, root, order) { // Thêm tham số
    const response = await fetch(`${API_BASE_URL}/horner/all-derivatives`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ coeffs, root, order }), // Gửi đủ tham số
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

export async function calculateReverseHorner(coeffs, root) {
    const response = await fetch(`${API_BASE_URL}/horner/reverse-horner`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ coeffs, root }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

export async function calculateWFunction(roots) {
    const response = await fetch(`${API_BASE_URL}/horner/w-function`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ roots }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

export async function calculateLagrangeInterpolation(xNodes, yNodes) {
    const response = await fetch(`${API_BASE_URL}/interpolation/lagrange`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x_nodes: xNodes, y_nodes: yNodes }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

export async function calculateDividedDifference(xNodes, yNodes) {
    const response = await fetch(`${API_BASE_URL}/interpolation/divided-difference`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x_nodes: xNodes, y_nodes: yNodes }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

export async function calculateFiniteDifference(xNodes, yNodes) {
    const response = await fetch(`${API_BASE_URL}/interpolation/finite-difference`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x_nodes: xNodes, y_nodes: yNodes }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

export async function calculateChangeVariables(coeffs, a, b) {
    const response = await fetch(`${API_BASE_URL}/horner/change-variables`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ coeffs, a, b }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

export async function calculateNewtonInterpolation(xNodes, yNodes, methodType) { // <<< THÊM methodType
    const response = await fetch(`${API_BASE_URL}/interpolation/newton-interpolation`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            x_nodes: xNodes,
            y_nodes: yNodes,
            method_type: methodType // <<< GỬI methodType
        }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

export async function calculateCentralInterpolation(xNodes, yNodes, methodType) { // <<< THÊM HÀM MỚI
    const response = await fetch(`${API_BASE_URL}/interpolation/central-interpolation`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            x_nodes: xNodes,
            y_nodes: yNodes,
            method_type: methodType
        }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

/**
 * Gửi yêu cầu tính toán Hàm ghép trơn (Spline).
 * @param {object} payload - Dữ liệu yêu cầu (x_nodes, y_nodes, spline_type, điều kiện biên...).
 * @returns {Promise<object>}
 */
export async function calculateSpline(payload) {
    const response = await fetch(`${API_BASE_URL}/interpolation/spline`, {
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
 * Gửi yêu cầu tính toán Bình phương tối thiểu.
 * @param {string} xNodes - Chuỗi các mốc x.
 * @param {string} yNodes - Chuỗi các giá trị y.
 * @param {string[]} basisFuncs - Mảng các chuỗi hàm cơ sở.
 * @returns {Promise<object>}
 */
export async function calculateLeastSquares(xNodes, yNodes, basisFuncs) {
    const response = await fetch(`${API_BASE_URL}/interpolation/least-squares`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            x_nodes: xNodes,
            y_nodes: yNodes,
            basis_funcs: basisFuncs // Gửi dưới dạng mảng các chuỗi
        }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định.');
    }
    return response.json();
}

/**
 * Gửi yêu cầu trích xuất mốc nội suy từ file.
 * @param {FormData} formData - Đối tượng FormData chứa file và các tham số.
 * @returns {Promise<object>}
 */
export async function calculateNodeSelection(formData) {
    const response = await fetch(`${API_BASE_URL}/interpolation/select-nodes`, {
        method: 'POST',
        body: formData, // Không cần 'Content-Type', trình duyệt sẽ tự đặt
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định từ máy chủ.');
    }
    
    return response.json();
}

/**
 * Gửi yêu cầu tìm khoảng cách ly nghiệm từ file.
 * @param {FormData} formData - Đối tượng FormData chứa file và giá trị y_bar.
 * @returns {Promise<object>}
 */
export async function calculateFindIntervals(formData) { // <-- THÊM MỚI
    const response = await fetch(`${API_BASE_URL}/interpolation/find-intervals`, {
        method: 'POST',
        body: formData, // Không cần 'Content-Type', trình duyệt sẽ tự đặt
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Lỗi không xác định từ máy chủ.');
    }
    
    return response.json();
}

/**
 * Gửi yêu cầu tính toán Nội suy ngược Lặp.
 * @param {object} payload - Dữ liệu yêu cầu (x_nodes, y_nodes, y_bar, epsilon, method).
 * @returns {Promise<object>}
 */
export async function calculateInverseInterpolation(payload) {
    const response = await fetch(`${API_BASE_URL}/interpolation/inverse-iterative`, {
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