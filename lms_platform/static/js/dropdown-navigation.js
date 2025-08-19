/**
 * Dropdown Navigation Functionality
 * Handles click-based dropdown menus and mobile navigation
 */

// Desktop dropdown functionality
function toggleDropdown() {
    const dropdown = document.getElementById('staffPortalDropdown');
    dropdown.classList.toggle('active');
}

// Mobile menu functionality
function toggleMobileMenu() {
    const overlay = document.getElementById('mobileNavOverlay');
    const menu = document.getElementById('mobileNavMenu');
    const body = document.body;
    
    overlay.classList.toggle('active');
    menu.classList.toggle('active');
    body.classList.toggle('mobile-menu-open');
}

function closeMobileMenu() {
    const overlay = document.getElementById('mobileNavOverlay');
    const menu = document.getElementById('mobileNavMenu');
    const body = document.body;
    
    overlay.classList.remove('active');
    menu.classList.remove('active');
    body.classList.remove('mobile-menu-open');
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('staffPortalDropdown');
    if (dropdown) {
        const isClickInsideDropdown = dropdown.contains(event.target);
        
        if (!isClickInsideDropdown) {
            dropdown.classList.remove('active');
        }
    }
});

// Close dropdown when pressing Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        // Close desktop dropdown
        const dropdown = document.getElementById('staffPortalDropdown');
        if (dropdown) {
            dropdown.classList.remove('active');
        }
        
        // Close mobile menu
        closeMobileMenu();
    }
});

// Close mobile menu when clicking overlay
document.addEventListener('click', function(event) {
    if (event.target.id === 'mobileNavOverlay') {
        closeMobileMenu();
    }
});

// Close dropdown when clicking on a dropdown item
document.addEventListener('click', function(event) {
    if (event.target.closest('.dropdown-item')) {
        const dropdown = document.getElementById('staffPortalDropdown');
        if (dropdown) {
            dropdown.classList.remove('active');
        }
    }
});

// Close mobile menu when clicking on navigation links
document.addEventListener('click', function(event) {
    if (event.target.closest('.mobile-nav-link')) {
        // Add small delay to allow navigation to start
        setTimeout(closeMobileMenu, 150);
    }
});

// Handle window resize - close mobile menu if window becomes large
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        closeMobileMenu();
    }
});

// Smooth scrolling for anchor links
document.addEventListener('click', function(event) {
    const link = event.target.closest('a[href^="#"]');
    if (link) {
        event.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            
            // Close mobile menu after scrolling starts
            if (window.innerWidth <= 768) {
                setTimeout(closeMobileMenu, 150);
            }
        }
    }
});