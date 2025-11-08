import { calculateSpline } from '../api.js';
import { renderSplineSolution, showLoading, hideLoading, showError } from '../ui.js';
import { setupTabHandlers } from '../tab-handlers.js';

export function setupSplineHandlers() {
    // 1. Setup tab chuyển đổi (Cấp 1, Cấp 2, Cấp 3)
    setupTabHandlers({
        tabClass: '.spline-tab',
        contentClass: '.spline-tab-content',
        activeTextColor: 'text-cyan-600', 
        activeBorderColor: 'border-cyan-500',
        container: document.getElementById('spline-interpolation-page')
    });

    // 2. Gắn sự kiện cho các nút tính toán
    const btnLinear = document.getElementById('calculate-spline-linear-btn');
    if (btnLinear) {
        btnLinear.addEventListener('click', () => handleSplineCalculation('linear'));
    }

    const btnQuad = document.getElementById('calculate-spline-quadratic-btn');
    if (btnQuad) {
        btnQuad.addEventListener('click', () => handleSplineCalculation('quadratic'));
    }

    const btnCubic = document.getElementById('calculate-spline-cubic-btn');
    if (btnCubic) {
        btnCubic.addEventListener('click', () => handleSplineCalculation('cubic'));
    }
}

async function handleSplineCalculation(splineType) {
    const xNodes = document.getElementById('spline-x-nodes').value;
    const yNodes = document.getElementById('spline-y-nodes').value;
    const resultsArea = document.getElementById('results-area');

    if (!xNodes.trim() || !yNodes.trim()) {
        showError('Vui lòng nhập đầy đủ các mốc x và giá trị y.');
        return;
    }

    const payload = {
        x_nodes: xNodes,
        y_nodes: yNodes,
        spline_type: splineType
    };

    if (splineType === 'quadratic') {
        payload.boundary_m1 = document.getElementById('spline-quad-boundary').value;
    } else if (splineType === 'cubic') {
        payload.boundary_start = document.getElementById('spline-cubic-boundary1').value;
        payload.boundary_end = document.getElementById('spline-cubic-boundary2').value;
    }

    showLoading();
    try {
        const data = await calculateSpline(payload);
        renderSplineSolution(resultsArea, data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}