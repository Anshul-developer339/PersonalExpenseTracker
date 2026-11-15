// Transactions-specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initTransactionsPage();
});

function initTransactionsPage() {
    // Initialize filter form
    initFilterForm();
    
    // Initialize search functionality
    initSearch();
    
    // Initialize delete confirmations
    initDeleteConfirmations();
    
    // Initialize category filter
    initCategoryFilter();
}

// Filter form functionality
function initFilterForm() {
    var filterForm = document.querySelector('form[method="GET"]');
    
    if (filterForm) {
        // Auto-submit on change for select inputs
        var selectInputs = filterForm.querySelectorAll('select');
        selectInputs.forEach(function(select) {
            select.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }
}

// Search functionality with debounce
function initSearch() {
    var searchInput = document.querySelector('input[name="search"]');
    
    if (searchInput) {
        var debouncedSearch = window.appUtils.debounce(function() {
            searchInput.form.submit();
        }, 500);
        
        searchInput.addEventListener('input', debouncedSearch);
    }
}

// Delete confirmation
function initDeleteConfirmations() {
    var deleteForms = document.querySelectorAll('form[action*="/delete/"]');
    
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var message = form.getAttribute('data-confirm') || 
                         'Are you sure you want to delete this transaction?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// Category filter
function initCategoryFilter() {
    var typeSelect = document.querySelector('select[name="type"]');
    var categorySelect = document.querySelector('select[name="category"]');
    
    if (typeSelect && categorySelect) {
        typeSelect.addEventListener('change', function() {
            updateCategoryOptions(this.value, categorySelect);
        });
    }
}

// Update category options based on transaction type
function updateCategoryOptions(type, categorySelect) {
    var incomeCategories = ['Salary', 'Freelancing', 'Business', 'Investment', 'Gift', 'Other'];
    var expenseCategories = ['Food', 'Shopping', 'Transportation', 'Education', 'Entertainment', 'Healthcare', 'Rent', 'Bills', 'Travel', 'Other'];
    
    var categories = type === 'income' ? incomeCategories : expenseCategories;
    
    // Clear existing options
    categorySelect.innerHTML = '<option value="">All Categories</option>';
    
    // Add new options
    categories.forEach(function(category) {
        var option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        categorySelect.appendChild(option);
    });
}

// Export transactions
function exportTransactions(format) {
    if (format === 'csv') {
        window.location.href = '/analytics/export/csv';
    }
}

// Bulk actions
function initBulkActions() {
    var selectAllCheckbox = document.querySelector('#select-all');
    var itemCheckboxes = document.querySelectorAll('.select-item');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            itemCheckboxes.forEach(function(checkbox) {
                checkbox.checked = selectAllCheckbox.checked;
            });
        });
    }
}

// Sort transactions
function sortTransactions(field, direction) {
    var url = new URL(window.location.href);
    url.searchParams.set('sort', field);
    url.searchParams.set('order', direction);
    window.location.href = url.toString();
}

// View transaction details
function viewTransactionDetails(transactionId) {
    // This could open a modal with transaction details
    console.log('Viewing transaction:', transactionId);
}

// Duplicate transaction
function duplicateTransaction(transactionId) {
    if (confirm('Do you want to duplicate this transaction?')) {
        window.location.href = '/transactions/duplicate/' + transactionId;
    }
}
