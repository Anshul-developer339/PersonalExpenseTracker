from app.models.budget import Budget
from app.models.transaction import Transaction
from app.extensions import db


class BudgetService:
    """Service layer for budget operations"""
    
    @staticmethod
    def create_budget(user_id, category, monthly_limit, month, year):
        """Create a new budget"""
        budget = Budget(
            user_id=user_id,
            category=category,
            monthly_limit=monthly_limit,
            month=month,
            year=year
        )
        db.session.add(budget)
        db.session.commit()
        return budget
    
    @staticmethod
    def get_user_budgets(user_id, month=None, year=None):
        """Get budgets for a user, optionally filtered by month/year"""
        query = Budget.query.filter_by(user_id=user_id)
        if month:
            query = query.filter_by(month=month)
        if year:
            query = query.filter_by(year=year)
        return query.order_by(Budget.category).all()
    
    @staticmethod
    def get_budget_by_id(budget_id, user_id):
        """Get a specific budget by ID for a user"""
        return Budget.query.filter_by(id=budget_id, user_id=user_id).first()
    
    @staticmethod
    def update_budget(budget, category, monthly_limit):
        """Update an existing budget"""
        budget.category = category
        budget.monthly_limit = monthly_limit
        db.session.commit()
        return budget
    
    @staticmethod
    def delete_budget(budget):
        """Delete a budget"""
        db.session.delete(budget)
        db.session.commit()
    
    @staticmethod
    def get_budget_spending(user_id, category, month, year):
        """Calculate actual spending for a category in a given month"""
        from datetime import date
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        result = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.category == category,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date < end_date
        ).with_entities(db.func.sum(Transaction.amount)).scalar()
        
        return result or 0.0
    
    @staticmethod
    def get_budget_utilization(budget):
        """Calculate budget utilization percentage"""
        spending = BudgetService.get_budget_spending(
            budget.user_id,
            budget.category,
            budget.month,
            budget.year
        )
        if budget.monthly_limit > 0:
            utilization = (spending / budget.monthly_limit) * 100
        else:
            utilization = 0
        return {
            'spent': spending,
            'remaining': max(0, budget.monthly_limit - spending),
            'utilization': min(100, utilization)
        }
