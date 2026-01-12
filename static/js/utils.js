/**
 * Vanilla JavaScript Utilities to Replace jQuery
 * Modern replacements for common jQuery operations
 */

// DOM Selection Utilities
const $ = (selector, context = document) => {
  return context.querySelector(selector);
};

const $$ = (selector, context = document) => {
  return Array.from(context.querySelectorAll(selector));
};

// DOM Ready
const ready = (callback) => {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', callback);
  } else {
    callback();
  }
};

// Event Delegation
const on = (element, event, selector, handler) => {
  element.addEventListener(event, (e) => {
    const target = e.target.closest(selector);
    if (target) {
      handler.call(target, e);
    }
  });
};

// AJAX Utilities using Fetch API
const ajax = {
  get: async (url, options = {}) => {
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('GET request failed:', error);
      throw error;
    }
  },

  post: async (url, data = {}, options = {}) => {
    try {
      const csrfToken = getCookie('csrftoken');
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
          ...options.headers
        },
        body: JSON.stringify(data),
        ...options
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('POST request failed:', error);
      throw error;
    }
  },

  formPost: async (url, formData, options = {}) => {
    try {
      const csrfToken = getCookie('csrftoken');
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          ...options.headers
        },
        body: formData,
        ...options
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Form POST request failed:', error);
      throw error;
    }
  }
};

// Get CSRF Token
const getCookie = (name) => {
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
};

// DOM Manipulation
const html = (element, content) => {
  if (typeof element === 'string') {
    element = $(element);
  }
  if (element) {
    element.innerHTML = content;
  }
};

const text = (element, content) => {
  if (typeof element === 'string') {
    element = $(element);
  }
  if (element) {
    element.textContent = content;
  }
};

const addClass = (element, className) => {
  if (typeof element === 'string') {
    element = $(element);
  }
  if (element) {
    element.classList.add(...className.split(' '));
  }
};

const removeClass = (element, className) => {
  if (typeof element === 'string') {
    element = $(element);
  }
  if (element) {
    element.classList.remove(...className.split(' '));
  }
};

const toggleClass = (element, className) => {
  if (typeof element === 'string') {
    element = $(element);
  }
  if (element) {
    element.classList.toggle(className);
  }
};

const hasClass = (element, className) => {
  if (typeof element === 'string') {
    element = $(element);
  }
  return element ? element.classList.contains(className) : false;
};

// Show/Hide elements
const show = (element, display = 'block') => {
  if (typeof element === 'string') {
    element = $(element);
  }
  if (element) {
    element.style.display = display;
  }
};

const hide = (element) => {
  if (typeof element === 'string') {
    element = $(element);
  }
  if (element) {
    element.style.display = 'none';
  }
};

const toggle = (element, display = 'block') => {
  if (typeof element === 'string') {
    element = $(element);
  }
  if (element) {
    element.style.display = element.style.display === 'none' ? display : 'none';
  }
};

// Form Utilities
const serializeForm = (form) => {
  if (typeof form === 'string') {
    form = $(form);
  }
  
  const formData = new FormData(form);
  const data = {};
  
  for (let [key, value] of formData.entries()) {
    if (data[key]) {
      if (!Array.isArray(data[key])) {
        data[key] = [data[key]];
      }
      data[key].push(value);
    } else {
      data[key] = value;
    }
  }
  
  return data;
};

// Animation Utilities
const fadeIn = (element, duration = 300) => {
  if (typeof element === 'string') {
    element = $(element);
  }
  
  if (!element) return;
  
  element.style.opacity = '0';
  element.style.display = 'block';
  
  let start = null;
  const animate = (timestamp) => {
    if (!start) start = timestamp;
    const progress = timestamp - start;
    element.style.opacity = Math.min(progress / duration, 1);
    
    if (progress < duration) {
      requestAnimationFrame(animate);
    }
  };
  
  requestAnimationFrame(animate);
};

const fadeOut = (element, duration = 300) => {
  if (typeof element === 'string') {
    element = $(element);
  }
  
  if (!element) return;
  
  let start = null;
  const animate = (timestamp) => {
    if (!start) start = timestamp;
    const progress = timestamp - start;
    element.style.opacity = Math.max(1 - progress / duration, 0);
    
    if (progress < duration) {
      requestAnimationFrame(animate);
    } else {
      element.style.display = 'none';
    }
  };
  
  requestAnimationFrame(animate);
};

// Debounce function
const debounce = (func, wait = 300) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// Throttle function
const throttle = (func, limit = 300) => {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};

// Loading Spinner
const showLoading = (container = 'body') => {
  const spinner = document.createElement('div');
  spinner.className = 'loading-overlay';
  spinner.innerHTML = `
    <div class="loading-spinner"></div>
  `;
  
  const target = typeof container === 'string' ? $(container) : container;
  if (target) {
    target.appendChild(spinner);
  }
};

const hideLoading = (container = 'body') => {
  const target = typeof container === 'string' ? $(container) : container;
  if (target) {
    const spinner = target.querySelector('.loading-overlay');
    if (spinner) {
      spinner.remove();
    }
  }
};

// Toast Notification
const showToast = (message, type = 'info', duration = 3000) => {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type} fade-in`;
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    box-shadow: var(--shadow-lg);
    z-index: 10000;
    max-width: 350px;
  `;
  
  toast.innerHTML = `
    <div style="display: flex; align-items: center; gap: 0.75rem;">
      <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
      <span>${message}</span>
    </div>
  `;
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    fadeOut(toast, 300);
    setTimeout(() => toast.remove(), 300);
  }, duration);
};

// Export utilities
window.utils = {
  $,
  $$,
  ready,
  on,
  ajax,
  getCookie,
  html,
  text,
  addClass,
  removeClass,
  toggleClass,
  hasClass,
  show,
  hide,
  toggle,
  serializeForm,
  fadeIn,
  fadeOut,
  debounce,
  throttle,
  showLoading,
  hideLoading,
  showToast
};
