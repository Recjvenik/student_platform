// Main JavaScript file for Student Platform

// CSRF Token setup for AJAX
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

// Setup AJAX with CSRF
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

// Form validation helper
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateMobile(mobile) {
    const re = /^[0-9]{10}$/;
    return re.test(mobile);
}

// Show/hide loading spinner
function showLoading() {
    if (!$('#loading-spinner').length) {
        $('body').append('<div id="loading-spinner" class="spinner"></div>');
    }
}

function hideLoading() {
    $('#loading-spinner').remove();
}

// Auto-save functionality for forms
let autoSaveTimer;
function enableAutoSave(formSelector, saveFunction, delay = 2000) {
    $(formSelector + ' input, ' + formSelector + ' select, ' + formSelector + ' textarea').on('change', function() {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(saveFunction, delay);
    });
}