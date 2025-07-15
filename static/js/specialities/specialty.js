/**
 * Specialty Pages Interactive JavaScript
 * Handles all interactive elements for specialty billing service pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive components
    initializeFAQ();
    initializeScrollAnimations();
    initializeSearch();
    initializeLoadingStates();
    initializeSmoothScrolling();
    initializeFormValidation();
    initializeTooltips();
    initializeAnalytics();

    console.log('🎯 Specialty page interactions initialized');
});

/**
 * FAQ Accordion Functionality
 */
function initializeFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach((item, index) => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        const icon = item.querySelector('.faq-icon');

        if (question && answer) {
            question.addEventListener('click', function() {
                const isActive = item.classList.contains('active');

                // Close all other FAQ items
                faqItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                        const otherAnswer = otherItem.querySelector('.faq-answer');
                        const otherIcon = otherItem.querySelector('.faq-icon');
                        if (otherAnswer) otherAnswer.style.maxHeight = '0';
                        if (otherIcon) otherIcon.classList.remove('ri-subtract-line');
                        if (otherIcon) otherIcon.classList.add('ri-add-line');
                    }
                });

                // Toggle current item
                if (isActive) {
                    item.classList.remove('active');
                    answer.style.maxHeight = '0';
                    if (icon) {
                        icon.classList.remove('ri-subtract-line');
                        icon.classList.add('ri-add-line');
                    }
                } else {
                    item.classList.add('active');
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                    if (icon) {
                        icon.classList.remove('ri-add-line');
                        icon.classList.add('ri-subtract-line');
                    }
                }

                // Track FAQ interaction
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'faq_toggle', {
                        'event_category': 'specialty_page',
                        'event_label': question.textContent.trim(),
                        'value': isActive ? 0 : 1
                    });
                }
            });

            // Add keyboard navigation
            question.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    question.click();
                }
            });
        }
    });
}

/**
 * Scroll-triggered animations
 */
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');

                // Add staggered animation delay for grid items
                if (entry.target.classList.contains('specialty-card') ||
                    entry.target.classList.contains('service-item')) {
                    const siblings = Array.from(entry.target.parentElement.children);
                    const index = siblings.indexOf(entry.target);
                    entry.target.style.animationDelay = `${index * 0.1}s`;
                }
            }
        });
    }, observerOptions);

    // Observe all elements with animation classes
    const animatedElements = document.querySelectorAll([
        '.specialty-card',
        '.service-item',
        '.process-step',
        '.challenge-card',
        '.solution-card',
        '.faq-item',
        '.animate-on-scroll'
    ].join(','));

    animatedElements.forEach(el => {
        el.classList.add('animate-on-scroll');
        observer.observe(el);
    });
}

/**
 * Search and filter functionality
 */
function initializeSearch() {
    const searchInput = document.querySelector('#specialty-search');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const specialtyCards = document.querySelectorAll('.specialty-card');

    if (searchInput) {
        let searchTimeout;

        searchInput.addEventListener('input', function(e) {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const searchTerm = e.target.value.toLowerCase();
                filterSpecialties(searchTerm);
            }, 300);
        });
    }

    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const filterType = this.dataset.filter;

            // Update active button
            filterButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            // Filter specialties
            filterSpecialties('', filterType);
        });
    });

    function filterSpecialties(searchTerm = '', filterType = 'all') {
        let visibleCount = 0;

        specialtyCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const description = card.querySelector('p').textContent.toLowerCase();
            const matchesSearch = !searchTerm || title.includes(searchTerm) || description.includes(searchTerm);
            const matchesFilter = filterType === 'all' || card.dataset.category === filterType;

            if (matchesSearch && matchesFilter) {
                card.style.display = 'block';
                card.style.animation = `fadeInUp 0.6s ease-out ${visibleCount * 0.1}s both`;
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Show no results message
        const noResults = document.querySelector('.no-results');
        if (noResults) {
            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
        }
    }
}

/**
 * Loading states and skeleton screens
 */
function initializeLoadingStates() {
    const loadingElements = document.querySelectorAll('.loading-skeleton');

    // Simulate loading for dynamic content
    setTimeout(() => {
        loadingElements.forEach(el => {
            el.classList.add('loaded');
        });
    }, 1000);

    // Handle form submissions
    const forms = document.querySelectorAll('form[data-async]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="ri-loader-line animate-spin mr-2"></i>Processing...';
            }
        });
    });
}

/**
 * Smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 100; // Account for fixed header

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });

                // Update URL without triggering scroll
                history.pushState(null, null, `#${targetId}`);

                // Focus management for accessibility
                setTimeout(() => {
                    targetElement.focus();
                }, 500);
            }
        });
    });
}

/**
 * Form validation and enhancement
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');

        inputs.forEach(input => {
            // Real-time validation
            input.addEventListener('blur', function() {
                validateField(this);
            });

            input.addEventListener('input', function() {
                // Clear error state on input
                this.classList.remove('error');
                const errorMsg = this.parentElement.querySelector('.error-message');
                if (errorMsg) errorMsg.remove();
            });
        });

        form.addEventListener('submit', function(e) {
            e.preventDefault();

            let isValid = true;
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });

            if (isValid) {
                // Handle form submission
                submitForm(form);
            }
        });
    });

    function validateField(field) {
        const value = field.value.trim();
        const rules = field.dataset.validate ? field.dataset.validate.split('|') : [];
        let isValid = true;
        let errorMessage = '';

        // Remove existing error
        field.classList.remove('error');
        const existingError = field.parentElement.querySelector('.error-message');
        if (existingError) existingError.remove();

        // Validate rules
        rules.forEach(rule => {
            if (!isValid) return;

            const [ruleName, ruleValue] = rule.split(':');

            switch (ruleName) {
                case 'required':
                    if (!value) {
                        isValid = false;
                        errorMessage = 'This field is required';
                    }
                    break;
                case 'email':
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (value && !emailRegex.test(value)) {
                        isValid = false;
                        errorMessage = 'Please enter a valid email address';
                    }
                    break;
                case 'phone':
                    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
                    if (value && !phoneRegex.test(value.replace(/[^\d+]/g, ''))) {
                        isValid = false;
                        errorMessage = 'Please enter a valid phone number';
                    }
                    break;
                case 'min':
                    if (value && value.length < parseInt(ruleValue)) {
                        isValid = false;
                        errorMessage = `Minimum ${ruleValue} characters required`;
                    }
                    break;
            }
        });

        if (!isValid) {
            field.classList.add('error');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-red-500 text-sm mt-1';
            errorDiv.textContent = errorMessage;
            field.parentElement.appendChild(errorDiv);
        }

        return isValid;
    }

    function submitForm(form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="ri-loader-line animate-spin mr-2"></i>Sending...';

        // Simulate API call
        setTimeout(() => {
            // Reset form
            form.reset();
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;

            // Show success message
            showNotification('Message sent successfully!', 'success');

            // Track form submission
            if (typeof gtag !== 'undefined') {
                gtag('event', 'form_submit', {
                    'event_category': 'specialty_page',
                    'event_label': form.dataset.formType || 'contact'
                });
            }
        }, 2000);
    }
}

/**
 * Tooltip functionality
 */
function initializeTooltips() {
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');

    tooltipTriggers.forEach(trigger => {
        let tooltip = null;

        trigger.addEventListener('mouseenter', function() {
            const text = this.dataset.tooltip;
            if (!text) return;

            tooltip = document.createElement('div');
            tooltip.className = 'tooltip absolute z-50 bg-gray-800 text-white text-sm px-3 py-2 rounded shadow-lg';
            tooltip.textContent = text;

            document.body.appendChild(tooltip);

            // Position tooltip
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';

            // Animation
            tooltip.style.opacity = '0';
            tooltip.style.transform = 'translateY(10px)';
            requestAnimationFrame(() => {
                tooltip.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                tooltip.style.opacity = '1';
                tooltip.style.transform = 'translateY(0)';
            });
        });

        trigger.addEventListener('mouseleave', function() {
            if (tooltip) {
                tooltip.style.opacity = '0';
                tooltip.style.transform = 'translateY(10px)';
                setTimeout(() => {
                    if (tooltip && tooltip.parentNode) {
                        tooltip.parentNode.removeChild(tooltip);
                    }
                }, 300);
            }
        });
    });
}

/**
 * Analytics tracking
 */
function initializeAnalytics() {
    // Track page views
    if (typeof gtag !== 'undefined') {
        gtag('config', 'GA_MEASUREMENT_ID', {
            page_title: document.title,
            page_location: window.location.href
        });
    }

    // Track specialty card clicks
    const specialtyCards = document.querySelectorAll('.specialty-card');
    specialtyCards.forEach(card => {
        card.addEventListener('click', function() {
            const specialtyName = this.querySelector('h3').textContent;
            if (typeof gtag !== 'undefined') {
                gtag('event', 'specialty_click', {
                    'event_category': 'specialty_selection',
                    'event_label': specialtyName
                });
            }
        });
    });

    // Track CTA button clicks
    const ctaButtons = document.querySelectorAll('.btn-specialty, .cta-button');
    ctaButtons.forEach(button => {
        button.addEventListener('click', function() {
            const buttonText = this.textContent.trim();
            if (typeof gtag !== 'undefined') {
                gtag('event', 'cta_click', {
                    'event_category': 'conversion',
                    'event_label': buttonText
                });
            }
        });
    });

    // Track scroll depth
    let maxScrollDepth = 0;
    let scrollDepthMarks = [25, 50, 75, 100];

    window.addEventListener('scroll', throttle(() => {
        const scrollTop = window.pageYOffset;
        const docHeight = document.body.offsetHeight;
        const winHeight = window.innerHeight;
        const scrollPercent = Math.round((scrollTop / (docHeight - winHeight)) * 100);

        if (scrollPercent > maxScrollDepth) {
            maxScrollDepth = scrollPercent;

            scrollDepthMarks.forEach(mark => {
                if (scrollPercent >= mark && typeof gtag !== 'undefined') {
                    gtag('event', 'scroll_depth', {
                        'event_category': 'engagement',
                        'event_label': `${mark}%`,
                        'value': mark
                    });
                    // Remove the mark to avoid duplicate tracking
                    scrollDepthMarks = scrollDepthMarks.filter(m => m !== mark);
                }
            });
        }
    }, 100));
}

/**
 * Utility functions
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transform translate-x-full transition-transform duration-300 ${
        type === 'success' ? 'bg-green-500 text-white' :
        type === 'error' ? 'bg-red-500 text-white' :
        'bg-blue-500 text-white'
    }`;

    notification.innerHTML = `
        <div class="flex items-center">
            <i class="ri-${type === 'success' ? 'check' : type === 'error' ? 'error-warning' : 'information'}-line mr-2"></i>
            <span>${message}</span>
            <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
                <i class="ri-close-line"></i>
            </button>
        </div>
    `;

    document.body.appendChild(notification);

    // Animate in
    requestAnimationFrame(() => {
        notification.style.transform = 'translateX(0)';
    });

    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(full)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

function debounce(func, wait, immediate) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Global function for FAQ toggle (fallback)
window.toggleFAQ = function(index) {
    const faqItem = document.querySelector(`.faq-item:nth-child(${index})`);
    if (faqItem) {
        const question = faqItem.querySelector('.faq-question');
        if (question) {
            question.click();
        }
    }
};

// Export functions for use in other modules
window.SpecialtyInteractions = {
    showNotification,
    throttle,
    debounce
};
