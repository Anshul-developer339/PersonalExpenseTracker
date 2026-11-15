from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.services.analytics_service import AnalyticsService
from app.services.transaction_service import TransactionService
from datetime import date, timedelta
import csv
from io import StringIO

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/')
@login_required
def index():
    """Analytics page"""
    user_id = current_user.id
    today = date.today()
    
    # Default to current year
    year = request.args.get('year', type=int) or today.year
    
    # Get yearly trend
    yearly_trend = AnalyticsService.get_yearly_trend(user_id, year)
    
    # Get category spending for current year
    start_of_year = date(year, 1, 1)
    end_of_year = date(year, 12, 31)
    category_spending = AnalyticsService.get_category_spending(user_id, start_of_year, end_of_year)
    
    # Get highest spending category
    highest_spending = AnalyticsService.get_highest_spending_category(user_id, start_of_year, end_of_year)
    
    # Get average monthly expenses
    avg_monthly_expenses = AnalyticsService.get_average_monthly_expenses(user_id, 6)
    
    # Get transaction counts
    transaction_counts = AnalyticsService.get_transaction_count_by_type(user_id, start_of_year, end_of_year)
    
    return render_template('analytics/index.html',
                         year=year,
                         yearly_trend=yearly_trend,
                         category_spending=category_spending,
                         highest_spending=highest_spending,
                         avg_monthly_expenses=avg_monthly_expenses,
                         transaction_counts=transaction_counts)


@analytics_bp.route('/api/data')
@login_required
def api_data():
    """API endpoint for analytics data"""
    user_id = current_user.id
    year = request.args.get('year', type=int) or date.today().year
    
    yearly_trend = AnalyticsService.get_yearly_trend(user_id, year)
    start_of_year = date(year, 1, 1)
    end_of_year = date(year, 12, 31)
    category_spending = AnalyticsService.get_category_spending(user_id, start_of_year, end_of_year)
    
    return jsonify({
        'yearly_trend': yearly_trend,
        'category_spending': category_spending
    })


@analytics_bp.route('/export/csv')
@login_required
def export_csv():
    """Export transactions as CSV"""
    from flask import Response
    
    user_id = current_user.id
    transactions = TransactionService.get_user_transactions(user_id).all()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Type', 'Category', 'Description', 'Amount'])
    
    for t in transactions:
        writer.writerow([
            t.transaction_date,
            t.type,
            t.category,
            t.description or '',
            t.amount
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=transactions_{date.today()}.csv'
        }
    )
