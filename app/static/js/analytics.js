// Analytics-specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initAnalyticsPage();
});

function initAnalyticsPage() {
    // Initialize year selector
    initYearSelector();
    
    // Initialize chart exports
    initChartExports();
    
    // Initialize data refresh
    initDataRefresh();
}

// Year selector
function initYearSelector() {
    var yearSelect = document.querySelector('select[name="year"]');
    
    if (yearSelect) {
        yearSelect.addEventListener('change', function() {
            this.form.submit();
        });
    }
}

// Chart export functionality
function initChartExports() {
    var exportButtons = document.querySelectorAll('.chart-export-btn');
    
    exportButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var chartId = this.getAttribute('data-chart-id');
            var filename = this.getAttribute('data-filename') || 'chart.png';
            exportChartAsImage(chartId, filename);
        });
    });
}

// Export chart as image
function exportChartAsImage(canvasId, filename) {
    var canvas = document.getElementById(canvasId);
    if (canvas) {
        var link = document.createElement('a');
        link.download = filename;
        link.href = canvas.toDataURL('image/png');
        link.click();
    }
}

// Refresh analytics data
function initDataRefresh() {
    var refreshBtn = document.querySelector('.refresh-analytics-btn');
    
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            refreshAnalyticsData();
        });
    }
}

// Refresh analytics data via AJAX
function refreshAnalyticsData() {
    var year = document.querySelector('select[name="year"]').value;
    var refreshBtn = document.querySelector('.refresh-analytics-btn');
    
    window.appUtils.showLoading(refreshBtn);
    
    fetch('/analytics/api/data?year=' + year)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            updateCharts(data);
            window.appUtils.hideLoading(refreshBtn, 'Refresh');
        })
        .catch(function(error) {
            console.error('Error:', error);
            window.appUtils.hideLoading(refreshBtn, 'Refresh');
            alert('Failed to refresh data');
        });
}

// Update charts with new data
function updateCharts(data) {
    // Update yearly trend chart
    if (window.yearlyTrendChart) {
        window.yearlyTrendChart.data.labels = data.yearly_trend.map(function(t) {
            return t.month;
        });
        window.yearlyTrendChart.data.datasets[0].data = data.yearly_trend.map(function(t) {
            return t.income;
        });
        window.yearlyTrendChart.data.datasets[1].data = data.yearly_trend.map(function(t) {
            return t.expenses;
        });
        window.yearlyTrendChart.update();
    }
    
    // Update category spending chart
    if (window.categorySpendingChart) {
        window.categorySpendingChart.data.labels = data.category_spending.map(function(c) {
            return c.category;
        });
        window.categorySpendingChart.data.datasets[0].data = data.category_spending.map(function(c) {
            return c.amount;
        });
        window.categorySpendingChart.update();
    }
}

// Export CSV
function exportCSV() {
    window.location.href = '/analytics/export/csv';
}

// Export PDF (placeholder for future implementation)
function exportPDF() {
    alert('PDF export feature coming soon!');
}

// Compare periods
function comparePeriods(period1, period2) {
    // This could compare two different time periods
    console.log('Comparing', period1, 'and', period2);
}

// Generate report
function generateReport(type) {
    var year = document.querySelector('select[name="year"]').value;
    
    if (type === 'monthly') {
        // Generate monthly report
        console.log('Generating monthly report for', year);
    } else if (type === 'yearly') {
        // Generate yearly report
        console.log('Generating yearly report for', year);
    }
}

// Share analytics
function shareAnalytics() {
    // Generate a shareable link or export data
    if (navigator.share) {
        navigator.share({
            title: 'My Expense Analytics',
            text: 'Check out my spending analytics',
            url: window.location.href
        }).catch(function(error) {
            console.log('Error sharing:', error);
        });
    } else {
        // Fallback: copy URL to clipboard
        window.appUtils.copyToClipboard(window.location.href);
    }
}

// Print analytics
function printAnalytics() {
    window.print();
}

// Toggle chart type
function toggleChartType(chartId, newType) {
    var chart = Chart.getChart(chartId);
    if (chart) {
        chart.config.type = newType;
        chart.update();
    }
}

// Filter by date range
function filterByDateRange(startDate, endDate) {
    var url = new URL(window.location.href);
    url.searchParams.set('start_date', startDate);
    url.searchParams.set('end_date', endDate);
    window.location.href = url.toString();
}

// Show/hide data points
function toggleDataPoints(chartId, datasetIndex) {
    var chart = Chart.getChart(chartId);
    if (chart) {
        var isVisible = chart.isDatasetVisible(datasetIndex);
        chart.toggleDataVisibility(datasetIndex);
        chart.update();
    }
}

// Reset filters
function resetFilters() {
    var url = new URL(window.location.href);
    url.search = '';
    window.location.href = url.toString();
}
