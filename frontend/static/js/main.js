// frontend/static/js/main.js
import { setupDirectMethodsHandlers } from './handlers/direct_methods_handler.js';
import { setupInverseMethodsHandlers } from './handlers/inverse_methods_handler.js';

/**
 * Ánh xạ từ data-page sang tiêu đề của trang.
 */
const PAGE_TITLES = {
    'matrix-solve-direct': 'Giải hệ phương trình (Phương pháp trực tiếp)',
    'matrix-solve-iterative': 'Giải hệ phương trình (Phương pháp lặp)',
    'matrix-inverse-direct': 'Tính ma trận nghịch đảo (Phương pháp trực tiếp)',
    'matrix-inverse-iterative': 'Tính ma trận nghịch đảo (Phương pháp lặp)',
    'matrix-svd': 'Phân tích SVD',
    'matrix-approximation': 'Ma trận xấp xỉ SVD',
    'matrix-eigen-methods': 'Tìm giá trị riêng & vector riêng',
    'nonlinear-solve': 'Giải phương trình f(x)=0',
    'polynomial-solve': 'Giải phương trình đa thức',
    'nonlinear-system-solve': 'Giải hệ phương trình phi tuyến',
    // Thêm các trang khác ở đây nếu cần
};

/**
 * Hàm chính để khởi tạo ứng dụng.
 */
document.addEventListener('DOMContentLoaded', function() {
    const sidebarMenu = document.getElementById('sidebar-menu');
    const mainContent = document.getElementById('main-content');
    const pageTitle = document.getElementById('page-title');

    if (sidebarMenu) {
        sidebarMenu.addEventListener('click', handleNavigation);
    }

    // Thiết lập trang mặc định khi tải lần đầu
    navigateToPage('matrix-solve-direct', mainContent, pageTitle);

    // Thiết lập các trình xử lý sự kiện cho các nút tính toán
    setupDirectMethodsHandlers();
    setupInverseMethodsHandlers();
    
    // Thêm các hàm setup khác cho các phương pháp khác ở đây
    // Ví dụ: setupIterativeMethodsHandlers();
    
    console.log("Ứng dụng đã sẵn sàng.");
});

/**
 * Xử lý sự kiện điều hướng khi nhấp vào menu.
 * @param {Event} event - Sự kiện click.
 */
function handleNavigation(event) {
    const target = event.target.closest('button[data-page]');
    if (!target) return; // Bỏ qua nếu không phải là nút điều hướng

    const pageId = target.dataset.page;
    const mainContent = document.getElementById('main-content');
    const pageTitle = document.getElementById('page-title');

    navigateToPage(pageId, mainContent, pageTitle);
}

/**
 * Chuyển đến một trang cụ thể.
 * @param {string} pageId - ID của trang cần hiển thị (từ data-page).
 * @param {HTMLElement} mainContentContainer - Vùng chứa nội dung chính.
 * @param {HTMLElement} titleElement - Phần tử h1 để cập nhật tiêu đề.
 */
function navigateToPage(pageId, mainContentContainer, titleElement) {
    const pageTemplate = document.getElementById(`${pageId}-page`);

    if (pageTemplate) {
        // Cập nhật tiêu đề trang
        titleElement.textContent = PAGE_TITLES[pageId] || 'Máy tính Giải tích số';

        // Cập nhật nội dung chính
        mainContentContainer.innerHTML = pageTemplate.innerHTML;

        // Xóa kết quả cũ và thông báo lỗi (nếu có)
        const resultsArea = mainContentContainer.querySelector('#results-area');
        const errorDiv = mainContentContainer.querySelector('#error-message');
        if (resultsArea) resultsArea.innerHTML = '';
        if (errorDiv) errorDiv.classList.add('hidden');
        
        // **Quan trọng**: Sau khi chèn nội dung mới, phải gắn lại các trình xử lý sự kiện
        // vì các phần tử cũ đã bị thay thế.
        rebindEventHandlers(mainContentContainer);

    } else {
        console.error(`Không tìm thấy template cho trang: ${pageId}-page`);
        mainContentContainer.innerHTML = `<p class="text-red-500">Lỗi: Không thể tải nội dung trang.</p>`;
    }
}

/**
 * Gắn lại các trình xử lý sự kiện cho các nút trong nội dung vừa được tải.
 * Điều này cần thiết vì innerHTML sẽ tạo ra các phần tử mới.
 * @param {HTMLElement} container - Vùng chứa nội dung.
 */
function rebindEventHandlers(container) {
    // Chỉ cần gọi lại hàm setup cho nhóm phương pháp tương ứng
    // Trong trường hợp này là các phương pháp trực tiếp
    setupDirectMethodsHandlers();
    setupInverseMethodsHandlers();
    // Khi bạn thêm các file handler khác, hãy gọi chúng ở đây
    // setupIterativeMethodsHandlers();
    // setupEigenMethodsHandlers();
}