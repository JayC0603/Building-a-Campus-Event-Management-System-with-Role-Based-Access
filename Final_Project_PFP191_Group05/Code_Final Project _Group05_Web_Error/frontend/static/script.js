/**
 * Main JavaScript file for Campus Event Management System
 */

// Global variables
let currentUser = null;
let currentEvents = [];

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadSystemInfo();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Check if user is logged in
    checkAuthStatus();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize date inputs with current date
    initializeDateInputs();
    
    // Load initial data
    loadInitialData();
}

/**
 * Setup global event listeners
 */
function setupEventListeners() {
    // Search functionality
    const searchInputs = document.querySelectorAll('[id*="search"]');
    searchInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const searchFunction = this.getAttribute('data-search-function');
                if (searchFunction && typeof window[searchFunction] === 'function') {
                    window[searchFunction]();
                }
            }
        });
    });

    // Filter change listeners
    const filterSelects = document.querySelectorAll('[id*="filter"]');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            const filterFunction = this.getAttribute('data-filter-function');
            if (filterFunction && typeof window[filterFunction] === 'function') {
                window[filterFunction]();
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                return false;
            }
        });
    });
}

/**
 * Check authentication status
 */
function checkAuthStatus() {
    fetch('/api/system/info')
        .then(response => response.json())
        .then(info => {
            currentUser = info.current_user;
            updateUIForUser();
        })
        .catch(error => {
            console.error('Error checking auth status:', error);
        });
}

/**
 * Update UI based on user status
 */
function updateUIForUser() {
    if (currentUser) {
        // User is logged in
        updateUserSpecificUI();
    } else {
        // User is not logged in
        hideAuthRequiredElements();
    }
}

/**
 * Update UI for logged in user
 */
function updateUserSpecificUI() {
    // Update user display elements
    const userElements = document.querySelectorAll('[data-user-info]');
    userElements.forEach(element => {
        const property = element.getAttribute('data-user-info');
        if (currentUser[property]) {
            element.textContent = currentUser[property];
        }
    });

    // Show/hide elements based on user role
    const roleElements = document.querySelectorAll('[data-role]');
    roleElements.forEach(element => {
        const requiredRole = element.getAttribute('data-role');
        if (currentUser.role === requiredRole) {
            element.style.display = '';
        } else {
            element.style.display = 'none';
        }
    });
}

/**
 * Hide elements that require authentication
 */
function hideAuthRequiredElements() {
    const authElements = document.querySelectorAll('[data-auth-required]');
    authElements.forEach(element => {
        element.style.display = 'none';
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize date inputs
 */
function initializeDateInputs() {
    const dateInputs = document.querySelectorAll('input[type="datetime-local"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            const now = new Date();
            now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
            input.min = now.toISOString().slice(0, 16);
            
            // Set default to 1 hour from now
            now.setHours(now.getHours() + 1);
            input.value = now.toISOString().slice(0, 16);
        }
    });
}

/**
 * Load initial data
 */
function loadInitialData() {
    loadSystemInfo();
}

/**
 * Load system information
 */
function loadSystemInfo() {
    fetch('/api/system/info')
        .then(response => response.json())
        .then(info => {
            updateSystemStats(info);
        })
        .catch(error => {
            console.error('Error loading system info:', error);
        });
}

/**
 * Update system statistics in UI
 */
function updateSystemStats(info) {
    // Update stats counters
    const statsElements = document.querySelectorAll('[data-stat]');
    statsElements.forEach(element => {
        const statType = element.getAttribute('data-stat');
        if (info[statType] !== undefined) {
            element.textContent = info[statType];
        }
    });
}

/**
 * Validate form before submission
 */
function validateForm(form) {
    let isValid = true;
    
    // Check required fields
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'Trường này là bắt buộc');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });

    // Validate email fields
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !isValidEmail(field.value)) {
            showFieldError(field, 'Email không hợp lệ');
            isValid = false;
        }
    });

    // Validate datetime fields
    const datetimeFields = form.querySelectorAll('input[type="datetime-local"]');
    datetimeFields.forEach(field => {
        if (field.value) {
            const eventDate = new Date(field.value);
            const now = new Date();
            if (eventDate <= now) {
                showFieldError(field, 'Ngày sự kiện phải là thời gian trong tương lai');
                isValid = false;
            }
        }
    });

    // Validate number fields
    const numberFields = form.querySelectorAll('input[type="number"]');
    numberFields.forEach(field => {
        if (field.value) {
            const value = parseInt(field.value);
            const min = parseInt(field.getAttribute('min') || 0);
            const max = parseInt(field.getAttribute('max') || Infinity);
            
            if (value < min) {
                showFieldError(field, `Giá trị phải >= ${min}`);
                isValid = false;
            } else if (value > max) {
                showFieldError(field, `Giá trị phải <= ${max}`);
                isValid = false;
            }
        }
    });

    return isValid;
}

/**
 * Show field validation error
 */
function showFieldError(field, message) {
    // Remove existing error
    clearFieldError(field);
    
    // Add error class
    field.classList.add('is-invalid');
    
    // Create error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    // Insert after field
    field.parentNode.insertBefore(errorDiv, field.nextSibling);
}

/**
 * Clear field validation error
 */
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    
    // Remove error message
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Format date for display (date only)
 */
function formatDateOnly(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN');
}

/**
 * Show success toast notification
 */
function showSuccess(message, duration = 5000) {
    showToast(message, 'success', duration);
}

/**
 * Show error toast notification
 */
function showError(message, duration = 5000) {
    showToast(message, 'error', duration);
}

/**
 * Show info toast notification
 */
function showInfo(message, duration = 5000) {
    showToast(message, 'info', duration);
}

/**
 * Show warning toast notification
 */
function showWarning(message, duration = 5000) {
    showToast(message, 'warning', duration);
}

/**
 * Generic toast notification function
 */
function showToast(message, type = 'info', duration = 5000) {
    // Create toast container if not exists
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }

    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white bg-${getBootstrapColor(type)} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas ${getToastIcon(type)} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    container.appendChild(toast);

    // Show toast
    const bsToast = new bootstrap.Toast(toast, {
        delay: duration
    });
    
    bsToast.show();

    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

/**
 * Get Bootstrap color class for toast type
 */
function getBootstrapColor(type) {
    const colors = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info'
    };
    return colors[type] || 'info';
}

/**
 * Get Font Awesome icon for toast type
 */
function getToastIcon(type) {
    const icons = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-triangle',
        'warning': 'fa-exclamation-circle',
        'info': 'fa-info-circle'
    };
    return icons[type] || 'fa-info-circle';
}

/**
 * Show loading spinner overlay
 */
function showLoading() {
    let overlay = document.getElementById('loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'spinner-overlay';
        overlay.innerHTML = `
            <div class="text-center">
                <div class="spinner-border spinner-border-lg text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Đang tải...</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }
    overlay.style.display = 'flex';
}

/**
 * Hide loading spinner overlay
 */
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

/**
 * Confirm dialog with custom message
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/**
 * Debounce function for search inputs
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}