from datetime import datetime, date
from app.models.transaction import Transaction
from app.extensions import db


class AnalyticsService:
    """Service layer for analytics operations"""
    
    @staticmethod
    def get_monthly_summary(user_id, year, month):
        """Get monthly income and expense summary"""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        income = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.type == 'income',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date < end_date
        ).with_entities(db.func.sum(Transaction.amount)).scalar() or 0.0
        
        expenses = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date < end_date
        ).with_entities(db.func.sum(Transaction.amount)).scalar() or 0.0
        
        return {
            'income': float(income),
            'expenses': float(expenses),
            'savings': float(income - expenses)
        }
    
    @staticmethod
    def get_yearly_trend(user_id, year):
        """Get monthly income/expense trend for a year"""
        monthly_data = []
        
        for month in range(1, 13):
            summary = AnalyticsService.get_monthly_summary(user_id, year, month)
            monthly_data.append({
                'month': month,
                'income': summary['income'],
                'expenses': summary['expenses']
            })
        
        return monthly_data
    
    @staticmethod
    def get_category_spending(user_id, start_date=None, end_date=None):
        """Get expense breakdown by category"""
        query = Transaction.query.filter_by(user_id=user_id, type='expense')
        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)
        
        results = query.with_entities(
            Transaction.category,
            db.func.sum(Transaction.amount).label('total')
        ).group_by(Transaction.category).order_by(db.desc('total')).all()
        
        return [{'category': cat, 'amount': float(amt)} for cat, amt in results]
    
    @staticmethod
    def get_highest_spending_category(user_id, start_date=None, end_date=None):
        """Get the category with highest spending"""
        category_spending = AnalyticsService.get_category_spending(user_id, start_date, end_date)
        return category_spending[0] if category_spending else None
    
    @staticmethod
    def get_average_monthly_expenses(user_id, months=6):
        """Calculate average monthly expenses over given months"""
        today = date.today()
        total_expenses = 0.0
        
        for i in range(months):
            year = today.year
            month = today.month - i
            if month <= 0:
                month += 12
                year -= 1
            
            summary = AnalyticsService.get_monthly_summary(user_id, year, month)
            total_expenses += summary['expenses']
        
        return total_expenses / months if months > 0 else 0.0
    
    @staticmethod
    def get_transaction_count_by_type(user_id, start_date=None, end_date=None):
        """Get count of transactions by type"""
        query = Transaction.query.filter_by(user_id=user_id)
        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)
        
        results = query.with_entities(
            Transaction.type,
            db.func.count(Transaction.id).label('count')
        ).group_by(Transaction.type).all()
        
        return {t: count for t, count in results}
