//frontend/static/js/tab-handlers.js
export function setupTabHandlers(options = {
    tabClass: '.horner-tab', 
    contentClass: '.horner-tab-content',
    activeTextColor: 'text-red-600',
    activeBorderColor: 'border-red-500',
    container: document
}) {
    const root = options.container || document;
    const tabs = root.querySelectorAll(options.tabClass);
    if (!tabs || tabs.length === 0) return;

    const clearActive = () => {
        tabs.forEach(b => {
            b.classList.remove(options.activeTextColor, options.activeBorderColor);
            b.classList.add('text-gray-500', 'border-transparent');
            b.setAttribute('aria-selected', 'false');
        });
    };

    const setActive = (b) => {
        clearActive();
        b.classList.add(options.activeTextColor, options.activeBorderColor);
        b.classList.remove('text-gray-500', 'border-transparent');
        b.setAttribute('aria-selected', 'true');
    };

    tabs.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const tab = btn.dataset.tab;
            // hide all contents
            const contents = root.querySelectorAll(options.contentClass);
            contents.forEach(c => c.classList.add('hidden'));
            const active = root.querySelector(`#${tab}-content`);
            if (active) active.classList.remove('hidden');
            // update active tab styles
            setActive(btn);
        });
    });

    // ensure there is one active tab (use first if none)
    const anyActive = Array.from(tabs).some(b => 
        b.classList.contains(options.activeTextColor) || 
        b.getAttribute('aria-selected') === 'true'
    );
    if (!anyActive && tabs[0]) setActive(tabs[0]);
}

// Setup cho sidebar menu
export function setupSidebarHandlers() {
    const matrixMenuBtn = document.querySelector('.matrix-menu-btn');
    const matrixSubmenu = document.querySelector('.submenu-matrix');
    const matrixArrow = document.querySelector('.matrix-menu-arrow');

    matrixMenuBtn.addEventListener('click', (e) => {
        e.preventDefault();
        matrixSubmenu.classList.toggle('hidden');
        matrixArrow.style.transform = matrixSubmenu.classList.contains('hidden') 
            ? 'rotate(0deg)' 
            : 'rotate(180deg)';
    });
}