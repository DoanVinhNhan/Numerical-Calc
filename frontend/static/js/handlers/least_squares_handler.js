import { calculateLeastSquares } from '../api.js';
import { renderLsqSolution, showLoading, hideLoading, showError } from '../ui.js';

export function setupLeastSquaresHandlers() {
    const calculateBtn = document.getElementById('calculate-least-squares-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', handleLsqCalculation);
    }
}

async function handleLsqCalculation() {
    const xNodes = document.getElementById('lsq-x-nodes').value;
    const yNodes = document.getElementById('lsq-y-nodes').value;
    const basisFuncsRaw = document.getElementById('lsq-basis-funcs').value;
    const resultsArea = document.getElementById('results-area');

    // Tách các hàm cơ sở theo dòng và lọc bỏ các dòng trống
    const basisFuncs = basisFuncsRaw.split('\n').filter(f => f.trim() !== '');

    if (!xNodes.trim() || !yNodes.trim() || basisFuncs.length === 0) {
        showError('Vui lòng nhập đầy đủ mốc x, giá trị y, và ít nhất một hàm cơ sở.');
        return;
    }

    showLoading();
    try {
        const data = await calculateLeastSquares(xNodes, yNodes, basisFuncs);
        renderLsqSolution(resultsArea, data);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}