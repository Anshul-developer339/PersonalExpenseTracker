// Dashboard-specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Dashboard initialization
    initDashboard();
});

function initDashboard() {
    // Refresh dashboard data periodically (every 30 seconds)
    // Uncomment if you want auto-refresh
    // setInterval(refreshDashboard, 30000);
    
    // Add event listeners for interactive elements
    initQuickAddButton();
    initDateFilters();
}

// Quick add transaction button
function initQuickAddButton() {
    var quickAddBtn = document.querySelector('.position-fixed .btn-primary');
    
    if (quickAddBtn) {
        quickAddBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/transactions/add';
        });
    }
}

// Date filter functionality
function initDateFilters() {
    var startDateInput = document.querySelector('input[name="start_date"]');
    var endDateInput = document.querySelector('input[name="end_date"]');
    
    if (startDateInput && endDateInput) {
        // Set default date range (current month)
        var today = new Date();
        var firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
        var lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
        
        startDateInput.value = firstDay.toISOString().split('T')[0];
        endDateInput.value = lastDay.toISOString().split('T')[0];
    }
}

// Refresh dashboard data
function refreshDashboard() {
    // Make an AJAX request to refresh dashboard data
    // This would update the charts and summary cards without page reload
    console.log('Refreshing dashboard...');
}

// Export chart as image
function exportChartAsImage(canvasId, filename) {
    var canvas = document.getElementById(canvasId);
    if (canvas) {
        var link = document.createElement('a');
        link.download = filename || 'chart.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    }
}

// Initialize chart tooltips
function initChartTooltips(chart) {
    chart.options.plugins.tooltip = {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleFont: {
            size: 14,
            weight: 'bold'
        },
        bodyFont: {
            size: 12
        },
        padding: 12,
        cornerRadius: 8,
        displayColors: true
    };
}

// Responsive chart configuration
function getResponsiveChartConfig() {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'bottom',
                labels: {
                    padding: 20,
                    usePointStyle: true
                }
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)'
                }
            }
        }
    };
}
