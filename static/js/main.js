// ============================================
// STUDENT PLATFORM - MAIN JAVASCRIPT
// Modern | Mobile-First | Progressive Enhancement
// ============================================

(function() {
    'use strict';

    // ============================================
    // CSRF TOKEN SETUP
    // ============================================
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Setup AJAX with CSRF token
    if (typeof $ !== 'undefined') {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });
    }

    // ============================================
    // FORM VALIDATION UTILITIES
    // ============================================
    
    const Validators = {
        email: function(email) {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(email);
        },
        
        mobile: function(mobile) {
            // Indian mobile number: starts with 6-9, followed by 9 digits
            const re = /^[6-9]\d{9}$/;
            return re.test(mobile);
        },
        
        required: function(value) {
            return value !== null && value !== undefined && value.toString().trim() !== '';
        },
        
        minLength: function(value, min) {
            return value && value.length >= min;
        },
        
        maxLength: function(value, max) {
            return value && value.length <= max;
        },
        
        numeric: function(value) {
            return !isNaN(parseFloat(value)) && isFinite(value);
        },
        
        alphanumeric: function(value) {
            const re = /^[a-zA-Z0-9]+$/;
            return re.test(value);
        }
    };

    // ============================================
    // FORM ENHANCEMENTS
    // ============================================
    
    // Auto-format phone numbers
    function setupPhoneFormatting() {
        $('input[type="tel"]').on('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length > 10) {
                this.value = this.value.slice(0, 10);
            }
        });
    }

    // Real-time validation
    function setupRealtimeValidation() {
        // Email validation
        $('input[type="email"]').on('blur', function() {
            const $this = $(this);
            const email = $this.val().trim();
            
            if (email && !Validators.email(email)) {
                $this.css('border-color', 'var(--error)');
                showFieldError($this, 'Please enter a valid email address');
            } else {
                $this.css('border-color', '');
                hideFieldError($this);
            }
        });

        // Mobile validation
        $('input[type="tel"]').on('blur', function() {
            const $this = $(this);
            const mobile = $this.val().trim();
            
            if (mobile && !Validators.mobile(mobile)) {
                $this.css('border-color', 'var(--error)');
                showFieldError($this, 'Please enter a valid 10-digit mobile number');
            } else {
                $this.css('border-color', '');
                hideFieldError($this);
            }
        });

        // Required field validation
        $('input[required], select[required], textarea[required]').on('blur', function() {
            const $this = $(this);
            const value = $this.val();
            
            if (!Validators.required(value)) {
                $this.css('border-color', 'var(--error)');
            } else {
                $this.css('border-color', '');
            }
        });
    }

    function showFieldError($field, message) {
        const $error = $field.siblings('.error-text');
        if ($error.length) {
            $error.html('<i class="fa-solid fa-circle-exclamation"></i> ' + message).show();
        }
    }

    function hideFieldError($field) {
        const $error = $field.siblings('.error-text');
        if ($error.length) {
            $error.hide().text('');
        }
    }

    // ============================================
    // LOADING INDICATORS
    // ============================================
    
    const LoadingIndicator = {
        show: function(message = 'Loading...') {
            if ($('#loading-overlay').length === 0) {
                const html = `
                    <div id="loading-overlay" style="
                        position: fixed;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: rgba(0, 0, 0, 0.5);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        z-index: 9999;
                    ">
                        <div style="
                            background: white;
                            padding: 2rem;
                            border-radius: var(--radius-lg);
                            box-shadow: var(--shadow-xl);
                            text-align: center;
                            max-width: 300px;
                        ">
                            <div class="spinner spinner-primary" style="margin: 0 auto var(--space-3);"></div>
                            <p style="margin: 0; color: var(--text-primary); font-weight: 500;">${message}</p>
                        </div>
                    </div>
                `;
                $('body').append(html);
            }
        },
        
        hide: function() {
            $('#loading-overlay').fadeOut(200, function() {
                $(this).remove();
            });
        }
    };

    // ============================================
    // TOAST NOTIFICATIONS
    // ============================================
    
    const Toast = {
        show: function(message, type = 'info', duration = 3000) {
            const icons = {
                success: 'fa-check-circle',
                error: 'fa-times-circle',
                warning: 'fa-exclamation-triangle',
                info: 'fa-info-circle'
            };
            
            const colors = {
                success: 'var(--success)',
                error: 'var(--error)',
                warning: 'var(--warning)',
                info: 'var(--info)'
            };
            
            const $toast = $(`
                <div class="toast" style="
                    position: fixed;
                    bottom: 24px;
                    right: 24px;
                    background: white;
                    padding: 1rem 1.5rem;
                    border-radius: var(--radius-lg);
                    box-shadow: var(--shadow-xl);
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    max-width: 320px;
                    z-index: var(--z-tooltip);
                    animation: slideInUp 0.3s ease;
                    border-left: 4px solid ${colors[type]};
                ">
                    <i class="fa-solid ${icons[type]}" style="color: ${colors[type]}; font-size: 1.25rem;"></i>
                    <span style="flex: 1; color: var(--text-primary); font-weight: 500; font-size: 0.875rem;">${message}</span>
                    <button onclick="this.parentElement.remove()" style="
                        background: none;
                        border: none;
                        color: var(--text-muted);
                        cursor: pointer;
                        padding: 0;
                        width: 20px;
                        height: 20px;
                    ">
                        <i class="fa-solid fa-times"></i>
                    </button>
                </div>
            `);
            
            $('body').append($toast);
            
            if (duration > 0) {
                setTimeout(() => {
                    $toast.fadeOut(200, function() {
                        $(this).remove();
                    });
                }, duration);
            }
        }
    };

    // ============================================
    // AUTO-SAVE FUNCTIONALITY
    // ============================================
    
    let autoSaveTimer;
    function enableAutoSave(formSelector, saveCallback, delay = 2000) {
        $(formSelector).find('input, select, textarea').on('change input', function() {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(function() {
                if (typeof saveCallback === 'function') {
                    saveCallback();
                }
            }, delay);
        });
    }

    // ============================================
    // SMOOTH SCROLL
    // ============================================
    
    function setupSmoothScroll() {
        $('a[href^="#"]').on('click', function(e) {
            const target = $(this.getAttribute('href'));
            if (target.length) {
                e.preventDefault();
                $('html, body').animate({
                    scrollTop: target.offset().top - 80
                }, 400);
            }
        });
    }

    // ============================================
    // FORM SUBMIT PREVENTION (double-click)
    // ============================================
    
    function preventDoubleSubmit() {
        $('form').on('submit', function() {
            const $form = $(this);
            const $submitBtn = $form.find('button[type="submit"]');
            
            if ($form.data('submitted') === true) {
                return false;
            }
            
            $form.data('submitted', true);
            $submitBtn.prop('disabled', true);
            
            // Re-enable after 3 seconds as a failsafe
            setTimeout(() => {
                $form.data('submitted', false);
                $submitBtn.prop('disabled', false);
            }, 3000);
        });
    }

    // ============================================
    // ANIMATIONS ON SCROLL
    // ============================================
    
    function setupScrollAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1
        });

        document.querySelectorAll('.fade-in').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(el);
        });
    }

    // ============================================
    // COPY TO CLIPBOARD
    // ============================================
    
    function copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                Toast.show('Copied to clipboard!', 'success', 2000);
            }).catch(() => {
                Toast.show('Failed to copy', 'error', 2000);
            });
        } else {
            // Fallback for older browsers
            const $temp = $('<textarea>');
            $('body').append($temp);
            $temp.val(text).select();
            document.execCommand('copy');
            $temp.remove();
            Toast.show('Copied to clipboard!', 'success', 2000);
        }
    }

    // ============================================
    // INITIALIZE ON DOCUMENT READY
    // ============================================
    
    $(document).ready(function() {
        setupPhoneFormatting();
        setupRealtimeValidation();
        setupSmoothScroll();
        preventDoubleSubmit();
        
        if ('IntersectionObserver' in window) {
            setupScrollAnimations();
        }
        
        // Remove loading class from body if present
        $('body').removeClass('loading');
        
        // Auto-focus first input in forms
        $('form input:visible:enabled:first').focus();
    });

    // ============================================
    // EXPOSE PUBLIC API
    // ============================================
    
    window.StudentPlatform = {
        Validators: Validators,
        LoadingIndicator: LoadingIndicator,
        Toast: Toast,
        enableAutoSave: enableAutoSave,
        copyToClipboard: copyToClipboard
    };

})();