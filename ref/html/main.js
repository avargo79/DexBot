
// DexBot API Reference Interactive Features
document.addEventListener('DOMContentLoaded', function() {
    // Initialize collapsible containers
    initializeCollapsibleContainers();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
});

function initializeCollapsibleContainers() {
    const containers = document.querySelectorAll('.redoc-collapsable-container');
    
    containers.forEach(container => {
        const closedDiv = container.querySelector('.redoc-collapsable-container-closed');
        const openDiv = container.querySelector('.redoc-collapsable-container-open');
        
        if (closedDiv && openDiv) {
            // Initially hide open content
            openDiv.style.display = 'none';
            
            closedDiv.addEventListener('click', function() {
                const isOpen = openDiv.style.display !== 'none';
                
                if (isOpen) {
                    openDiv.style.display = 'none';
                    container.classList.add('closed-container');
                } else {
                    openDiv.style.display = 'block';
                    container.classList.remove('closed-container');
                }
            });
        }
    });
}

function initializeSearch() {
    // Add search functionality if needed
    console.log('Search functionality initialized');
}

function initializeSmoothScrolling() {
    // Add smooth scrolling to anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}
