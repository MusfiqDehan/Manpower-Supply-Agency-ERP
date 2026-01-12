/**
 * Common JavaScript patterns for Manpower Supply Agency ERP
 * Reusable functions for search, forms, and other common operations
 */

// Search functionality with debouncing
const initializeSearch = (formSelector, inputSelector, resultsSelector, debounceTime = 300) => {
  const searchForm = utils.$(formSelector);
  const searchInput = utils.$(inputSelector);
  const resultsContainer = utils.$(resultsSelector);
  
  if (!searchForm || !searchInput || !resultsContainer) {
    console.warn('Search elements not found:', { formSelector, inputSelector, resultsSelector });
    return;
  }
  
  // Prevent form submission
  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
  });
  
  // Debounced search function
  const performSearch = utils.debounce(async function() {
    const searchValue = searchInput.value.trim();
    
    // Skip if search value is empty
    if (!searchValue) {
      return;
    }
    
    try {
      const url = new URL(searchForm.action, window.location.origin);
      url.searchParams.set('search_value', searchValue);
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.search_list) {
        resultsContainer.innerHTML = data.search_list;
      }
    } catch (error) {
      console.error('Search error:', error);
      utils.showToast('Search failed. Please try again.', 'error');
    }
  }, debounceTime);
  
  // Attach input listener
  searchInput.addEventListener('input', performSearch);
};

// Form submission handler with AJAX
const handleFormSubmit = async (form, options = {}) => {
  const {
    onSuccess = () => {},
    onError = () => {},
    showLoading = true,
    resetForm = false
  } = options;
  
  if (showLoading) {
    utils.showLoading(form);
  }
  
  try {
    const formData = new FormData(form);
    const csrfToken = utils.getCookie('csrftoken');
    
    const response = await fetch(form.action, {
      method: form.method || 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (showLoading) {
      utils.hideLoading(form);
    }
    
    if (resetForm) {
      form.reset();
    }
    
    onSuccess(data);
  } catch (error) {
    if (showLoading) {
      utils.hideLoading(form);
    }
    
    console.error('Form submission error:', error);
    onError(error);
  }
};

// Initialize forms with AJAX submission
const initializeAjaxForm = (formSelector, options = {}) => {
  const form = utils.$(formSelector);
  
  if (!form) {
    console.warn('Form not found:', formSelector);
    return;
  }
  
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    await handleFormSubmit(form, options);
  });
};

// Modal handler
const openModal = (modalSelector) => {
  const modal = utils.$(modalSelector);
  if (modal) {
    // Use Bootstrap's modal if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
      const bsModal = new bootstrap.Modal(modal);
      bsModal.show();
    } else {
      modal.style.display = 'block';
      modal.classList.add('show');
    }
  }
};

const closeModal = (modalSelector) => {
  const modal = utils.$(modalSelector);
  if (modal) {
    if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
      const bsModal = bootstrap.Modal.getInstance(modal);
      if (bsModal) {
        bsModal.hide();
      }
    } else {
      modal.style.display = 'none';
      modal.classList.remove('show');
    }
  }
};

// Confirmation dialog
const confirmAction = async (message, options = {}) => {
  const {
    title = 'Confirm',
    confirmText = 'Yes',
    cancelText = 'No',
    type = 'warning'
  } = options;
  
  return new Promise((resolve) => {
    // Simple native confirm for now
    // Can be enhanced with a custom modal
    const result = confirm(message);
    resolve(result);
  });
};

// Delete action with confirmation
const handleDelete = async (url, options = {}) => {
  const {
    confirmMessage = 'Are you sure you want to delete this item?',
    onSuccess = () => {},
    onError = () => {}
  } = options;
  
  const confirmed = await confirmAction(confirmMessage);
  
  if (!confirmed) {
    return;
  }
  
  try {
    const csrfToken = utils.getCookie('csrftoken');
    
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    utils.showToast('Deleted successfully', 'success');
    onSuccess(data);
  } catch (error) {
    console.error('Delete error:', error);
    utils.showToast('Delete failed. Please try again.', 'error');
    onError(error);
  }
};

// Table row click handler
const initializeTableRowClick = (tableSelector, rowSelector, callback) => {
  const table = utils.$(tableSelector);
  
  if (!table) {
    console.warn('Table not found:', tableSelector);
    return;
  }
  
  utils.on(table, 'click', rowSelector, callback);
};

// Pagination handler
const handlePagination = async (url, containerSelector) => {
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    const container = utils.$(containerSelector);
    
    if (container && data.html) {
      container.innerHTML = data.html;
    }
  } catch (error) {
    console.error('Pagination error:', error);
    utils.showToast('Failed to load page. Please try again.', 'error');
  }
};

// Export common patterns
window.appPatterns = {
  initializeSearch,
  handleFormSubmit,
  initializeAjaxForm,
  openModal,
  closeModal,
  confirmAction,
  handleDelete,
  initializeTableRowClick,
  handlePagination
};
