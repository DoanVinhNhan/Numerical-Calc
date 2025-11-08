// frontend/static/js/handlers/node_selection_handler.js
import { calculateNodeSelection } from '../api.js';
import { renderNodeSelectionSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupNodeSelectionHandlers() {
    const calculateBtn = document.getElementById('calculate-node-selection-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleNodeSelectionCalculation);
    }
}

async function handleNodeSelectionCalculation() {
    const fileInput = document.getElementById('node-selection-file-input');
    const xBar = document.getElementById('node-selection-x-bar').value;
    const numNodes = document.getElementById('node-selection-num-nodes').value;
    const method = document.querySelector('input[name="node-selection-method"]:checked').value;
    const resultsArea = document.getElementById('results-area');

    // Kiểm tra file
    if (!fileInput.files || fileInput.files.length === 0) {
        showError('Vui lòng chọn một file dữ liệu.');
        return;
    }
    const file = fileInput.files[0];

    // Kiểm tra các tham số khác
    if (!xBar.trim() || !numNodes.trim()) {
        showError('Vui lòng nhập đầy đủ giá trị cần tính (x̄) và số mốc (k).');
        return;
    }

    // Tạo FormData để gửi file
    const formData = new FormData();
    formData.append('file', file);
    formData.append('x_bar', xBar);
    formData.append('num_nodes', numNodes);
    formData.append('method', method);

    showLoading();
    try {
        const data = await calculateNodeSelection(formData);
        renderNodeSelectionSolution(resultsArea, data); // Hàm render mới
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}