// Theme management
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update theme icon
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        themeIcon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Mobile menu toggle
function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbar-nav');
    if (navbarNav) {
        navbarNav.classList.toggle('active');
    }
}

// Tab management
function showTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });
    
    // Show selected tab content
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const html = document.documentElement;
    
    html.setAttribute('data-theme', savedTheme);
    
    // Update theme icon
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        themeIcon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
    
    // Auto-hide alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Form validation feedback
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea[data-auto-resize]');
    textareas.forEach(textarea => {
        textarea.style.overflow = 'hidden';
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
        // Trigger on load
        textarea.dispatchEvent(new Event('input'));
    });
    
    // Loading states for buttons
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Загрузка...';
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });
    });
    
    // Copy code functionality
    addCopyButtons();
    
    // Progress tracking
    trackLessonProgress();
});

// Add copy buttons to code blocks
function addCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        
        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn btn-sm btn-outline-secondary';
        copyBtn.style.position = 'absolute';
        copyBtn.style.top = '0.5rem';
        copyBtn.style.right = '0.5rem';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.title = 'Копировать код';
        
        copyBtn.addEventListener('click', function() {
            navigator.clipboard.writeText(block.textContent).then(() => {
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                }, 2000);
            });
        });
        
        block.parentNode.parentNode.insertBefore(wrapper, block.parentNode);
        wrapper.appendChild(block.parentNode);
        wrapper.appendChild(copyBtn);
    });
}

// Track lesson progress
function trackLessonProgress() {
    // Track time spent on lesson
    let startTime = Date.now();
    let isActive = true;
    
    // Track when user becomes inactive
    document.addEventListener('visibilitychange', function() {
        isActive = !document.hidden;
        if (isActive) {
            startTime = Date.now();
        }
    });
    
    // Save progress on page unload
    window.addEventListener('beforeunload', function() {
        const timeSpent = Math.floor((Date.now() - startTime) / 1000);
        if (timeSpent > 10 && isActive) { // Only count if spent more than 10 seconds
            localStorage.setItem('lesson_time_' + window.location.pathname, timeSpent);
        }
    });
}

// Utility functions
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
    
    if (hours > 0) {
        return `${hours}ч ${minutes}м`;
    } else if (minutes > 0) {
        return `${minutes}м ${remainingSeconds}с`;
    } else {
        return `${remainingSeconds}с`;
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + D for dark mode toggle
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        toggleTheme();
    }
    
    // ESC to close modals and dropdowns
    if (e.key === 'Escape') {
        // Close any open modals
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) bsModal.hide();
        });
        
        // Close any open dropdowns
        const dropdowns = document.querySelectorAll('.dropdown-menu.show');
        dropdowns.forEach(dropdown => {
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown.previousElementSibling);
            if (bsDropdown) bsDropdown.hide();
        });
    }
});

// Enhanced form handling
function enhanceForm(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return;
    
    // Add loading state
    form.addEventListener('submit', function() {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.classList.add('loading');
        }
    });
    
    // Real-time validation
    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });
}

function validateField(field) {
    const isValid = field.checkValidity();
    field.classList.remove('is-valid', 'is-invalid');
    field.classList.add(isValid ? 'is-valid' : 'is-invalid');
    
    // Show/hide custom error message
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.style.display = isValid ? 'none' : 'block';
    }
}

// Performance monitoring
function logPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page load time:', Math.round(perfData.loadEventEnd - perfData.fetchStart), 'ms');
            }, 0);
        });
    }
}

// Initialize performance monitoring in development
if (window.location.hostname === 'localhost') {
    logPerformance();
}

// Accessibility improvements
function improveAccessibility() {
    // Add skip links
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Перейти к основному содержимому';
    skipLink.className = 'sr-only sr-only-focusable btn btn-primary';
    skipLink.style.position = 'absolute';
    skipLink.style.top = '10px';
    skipLink.style.left = '10px';
    skipLink.style.zIndex = '9999';
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Add ARIA labels where missing
    const buttons = document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])');
    buttons.forEach(button => {
        if (!button.textContent.trim() && button.querySelector('i')) {
            const icon = button.querySelector('i');
            if (icon.classList.contains('fa-edit')) {
                button.setAttribute('aria-label', 'Редактировать');
            } else if (icon.classList.contains('fa-delete') || icon.classList.contains('fa-trash')) {
                button.setAttribute('aria-label', 'Удалить');
            } else if (icon.classList.contains('fa-plus')) {
                button.setAttribute('aria-label', 'Добавить');
            }
        }
    });
}

// Initialize accessibility improvements
document.addEventListener('DOMContentLoaded', improveAccessibility);
