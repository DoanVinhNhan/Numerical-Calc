// frontend/static/js/handlers/find_intervals_handler.js
import { calculateFindIntervals } from '../api.js';
import { renderFindIntervalsSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupFindIntervalsHandlers() {
    const calculateBtn = document.getElementById('calculate-find-intervals-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleFindIntervalsCalculation);
    }
}

async function handleFindIntervalsCalculation() {
    const fileInput = document.getElementById('find-intervals-file-input');
    const yBar = document.getElementById('find-intervals-y-bar').value;
    const num_nodes = document.getElementById('find-intervals-num-nodes').value;
    // const method = document.querySelector('input[name="find-intervals-method"]:checked').value; // <-- ĐÃ XÓA
    const resultsArea = document.getElementById('results-area');

    if (!fileInput.files || fileInput.files.length === 0) {
        showError('Vui lòng chọn một file dữ liệu.');
        return;
    }
    const file = fileInput.files[0];

    if (!yBar.trim()) {
        showError('Vui lòng nhập giá trị y cần tìm (ȳ).');
        return;
    }
    
    if (!num_nodes.trim()) {
        showError('Vui lòng nhập số mốc k.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('y_bar', yBar);
    formData.append('num_nodes', num_nodes);
    // formData.append('method', method); // <-- ĐÃ XÓA

    showLoading();
    try {
        const data = await calculateFindIntervals(formData);
        renderFindIntervalsSolution(resultsArea, data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}