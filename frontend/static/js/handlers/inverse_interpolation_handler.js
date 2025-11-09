// frontend/static/js/handlers/inverse_interpolation_handler.js
import { calculateInverseInterpolation } from '../api.js';
import { renderInverseInterpolationSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupInverseInterpolationHandlers() {
    const calculateBtn = document.getElementById('calculate-inv-inter-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleInverseIterCalculation);
    }
}

async function handleInverseIterCalculation() {
    const xNodes = document.getElementById('inv-inter-x-nodes').value;
    const yNodes = document.getElementById('inv-inter-y-nodes').value;
    const yBar = document.getElementById('inv-inter-y-bar').value;
    const epsilon = document.getElementById('inv-inter-epsilon').value;
    const resultsArea = document.getElementById('results-area');
    
    // Đảm bảo nút radio được chọn
    const methodRadio = document.querySelector('input[name="inv-inter-method"]:checked');
    if (!methodRadio) {
         showError('Vui lòng chọn phương pháp Newton Tiến hoặc Lùi.');
         return;
    }
    const method = methodRadio.value;

    if (!xNodes.trim() || !yNodes.trim() || !yBar.trim() || !epsilon.trim()) {
        showError('Vui lòng nhập đầy đủ các mốc x, y, giá trị ȳ và sai số ε.');
        return;
    }

    const payload = {
        x_nodes: xNodes,
        y_nodes: yNodes,
        y_bar: parseFloat(yBar),
        epsilon: parseFloat(epsilon),
        method: method
    };

    showLoading();
    try {
        const data = await calculateInverseInterpolation(payload);
        renderInverseInterpolationSolution(resultsArea, data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}