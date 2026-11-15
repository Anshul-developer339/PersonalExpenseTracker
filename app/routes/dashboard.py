from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.transaction_service import TransactionService
from app.services.analytics_service import AnalyticsService
from datetime import date, timedelta

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard page"""
    user_id = current_user.id
    today = date.today()
    
    # Current month dates
    start_of_month = date(today.year, today.month, 1)
    if today.month == 12:
        end_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
    else:
        end_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)
    
    # Calculate totals
    total_income = TransactionService.get_total_income(user_id)
    total_expenses = TransactionService.get_total_expenses(user_id)
    current_balance = total_income - total_expenses
    
    # Monthly calculations
    monthly_income = TransactionService.get_total_income(user_id, start_of_month, end_of_month)
    monthly_expenses = TransactionService.get_total_expenses(user_id, start_of_month, end_of_month)
    monthly_savings = monthly_income - monthly_expenses
    
    # Recent transactions (last 10)
    recent_transactions = TransactionService.get_user_transactions(user_id).limit(10).all()
    
    # Monthly trend for chart (last 6 months)
    monthly_trend = []
    for i in range(5, -1, -1):
        month = today.month - i
        year = today.year
        if month <= 0:
            month += 12
            year -= 1
        summary = AnalyticsService.get_monthly_summary(user_id, year, month)
        monthly_trend.append({
            'month': f"{year}-{month:02d}",
            'income': summary['income'],
            'expenses': summary['expenses']
        })
    
    # Category breakdown for pie chart
    category_breakdown = AnalyticsService.get_category_spending(user_id, start_of_month, end_of_month)
    
    return render_template('dashboard/index.html',
                         total_income=total_income,
                         total_expenses=total_expenses,
                         current_balance=current_balance,
                         monthly_income=monthly_income,
                         monthly_expenses=monthly_expenses,
                         monthly_savings=monthly_savings,
                         recent_transactions=recent_transactions,
                         monthly_trend=monthly_trend,
                         category_breakdown=category_breakdown)
