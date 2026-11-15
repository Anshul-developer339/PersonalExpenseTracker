// Budgets-specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initBudgetsPage();
});

function initBudgetsPage() {
    // Initialize month/year selector
    initMonthYearSelector();
    
    // Initialize budget form
    initBudgetForm();
    
    // Initialize budget progress bars animation
    initProgressBars();
    
    // Initialize budget edit modals
    initBudgetEdit();
}

// Month/year selector
function initMonthYearSelector() {
    var monthSelect = document.querySelector('select[name="month"]');
    var yearSelect = document.querySelector('select[name="year"]');
    
    if (monthSelect && yearSelect) {
        // Auto-submit on change
        monthSelect.addEventListener('change', function() {
            this.form.submit();
        });
        
        yearSelect.addEventListener('change', function() {
            this.form.submit();
        });
    }
}

// Budget form validation
function initBudgetForm() {
    var budgetForm = document.querySelector('form[action*="/budgets/add"]');
    
    if (budgetForm) {
        budgetForm.addEventListener('submit', function(e) {
            var amount = parseFloat(document.querySelector('input[name="monthly_limit"]').value);
            var category = document.querySelector('select[name="category"]').value;
            
            if (!category) {
                e.preventDefault();
                alert('Please select a category');
                return;
            }
            
            if (isNaN(amount) || amount <= 0) {
                e.preventDefault();
                alert('Please enter a valid amount greater than 0');
                return;
            }
        });
    }
}

// Animate progress bars
function initProgressBars() {
    var progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(function(bar) {
        var width = bar.style.width;
        bar.style.width = '0';
        
        setTimeout(function() {
            bar.style.transition = 'width 0.5s ease-in-out';
            bar.style.width = width;
        }, 100);
    });
}

// Budget edit functionality
function initBudgetEdit() {
    var editButtons = document.querySelectorAll('.budget-edit-btn');
    
    editButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var budgetId = this.getAttribute('data-budget-id');
            editBudget(budgetId);
        });
    });
}

// Edit budget
function editBudget(budgetId) {
    // This could open a modal for editing
    var budgetForm = document.querySelector('form[action*="/budgets/edit/' + budgetId + '"]');
    if (budgetForm) {
        budgetForm.submit();
    }
}

// Delete budget with confirmation
function deleteBudget(budgetId) {
    if (confirm('Are you sure you want to delete this budget?')) {
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = '/budgets/delete/' + budgetId;
        document.body.appendChild(form);
        form.submit();
    }
}

// Calculate budget utilization
function calculateUtilization(spent, limit) {
    if (limit === 0) return 0;
    return Math.min((spent / limit) * 100, 100);
}

// Get utilization color class
function getUtilizationClass(utilization) {
    if (utilization >= 100) return 'bg-danger';
    if (utilization >= 90) return 'bg-warning';
    if (utilization >= 75) return 'bg-info';
    return 'bg-success';
}

// Show budget warning
function showBudgetWarning(utilization) {
    if (utilization >= 100) {
        return 'Budget exceeded!';
    } else if (utilization >= 90) {
        return 'High spending warning!';
    } else if (utilization >= 75) {
        return 'Budget utilization warning!';
    }
    return null;
}

// Copy budget to next month
function copyBudgetToNextMonth(budgetId) {
    if (confirm('Copy this budget to the next month?')) {
        // Make an AJAX request to copy the budget
        window.appUtils.makeRequest('/budgets/copy/' + budgetId, {
            method: 'POST'
        }).then(function(data) {
            if (data.success) {
                alert('Budget copied successfully!');
                location.reload();
            } else {
                alert('Failed to copy budget');
            }
        }).catch(function(error) {
            console.error('Error:', error);
            alert('An error occurred');
        });
    }
}

// Budget suggestions based on spending
function getBudgetSuggestions(category, currentSpending) {
    // Suggest budget limits based on current spending patterns
    var suggestions = [
        { label: 'Same as current', value: currentSpending },
        { label: '+10%', value: currentSpending * 1.1 },
        { label: '+20%', value: currentSpending * 1.2 },
        { label: '+50%', value: currentSpending * 1.5 }
    ];
    
    return suggestions;
}
