from datetime import datetime
from app.models.transaction import Transaction
from app.extensions import db


class TransactionService:
    """Service layer for transaction operations"""
    
    @staticmethod
    def create_transaction(user_id, type, amount, category, description, transaction_date):
        """Create a new transaction"""
        transaction = Transaction(
            user_id=user_id,
            type=type,
            amount=amount,
            category=category,
            description=description,
            transaction_date=transaction_date
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction
    
    @staticmethod
    def get_user_transactions(user_id, filters=None):
        """Get transactions for a user with optional filters"""
        query = Transaction.query.filter_by(user_id=user_id)
        
        if filters:
            if 'type' in filters:
                query = query.filter_by(type=filters['type'])
            if 'category' in filters:
                query = query.filter_by(category=filters['category'])
            if 'start_date' in filters:
                query = query.filter(Transaction.transaction_date >= filters['start_date'])
            if 'end_date' in filters:
                query = query.filter(Transaction.transaction_date <= filters['end_date'])
            if 'search' in filters:
                search_term = f"%{filters['search']}%"
                query = query.filter(
                    (Transaction.description.ilike(search_term)) |
                    (Transaction.category.ilike(search_term))
                )
        
        return query.order_by(Transaction.transaction_date.desc())
    
    @staticmethod
    def get_transaction_by_id(transaction_id, user_id):
        """Get a specific transaction by ID for a user"""
        return Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    
    @staticmethod
    def update_transaction(transaction, type, amount, category, description, transaction_date):
        """Update an existing transaction"""
        transaction.type = type
        transaction.amount = amount
        transaction.category = category
        transaction.description = description
        transaction.transaction_date = transaction_date
        db.session.commit()
        return transaction
    
    @staticmethod
    def delete_transaction(transaction):
        """Delete a transaction"""
        db.session.delete(transaction)
        db.session.commit()
    
    @staticmethod
    def get_total_income(user_id, start_date=None, end_date=None):
        """Get total income for a user within date range"""
        query = Transaction.query.filter_by(user_id=user_id, type='income')
        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)
        result = query.with_entities(db.func.sum(Transaction.amount)).scalar()
        return result or 0.0
    
    @staticmethod
    def get_total_expenses(user_id, start_date=None, end_date=None):
        """Get total expenses for a user within date range"""
        query = Transaction.query.filter_by(user_id=user_id, type='expense')
        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)
        result = query.with_entities(db.func.sum(Transaction.amount)).scalar()
        return result or 0.0
    
    @staticmethod
    def get_category_breakdown(user_id, transaction_type, start_date=None, end_date=None):
        """Get spending/income breakdown by category"""
        query = Transaction.query.filter_by(user_id=user_id, type=transaction_type)
        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)
        
        results = query.with_entities(
            Transaction.category,
            db.func.sum(Transaction.amount).label('total')
        ).group_by(Transaction.category).all()
        
        return {category: float(total) for category, total in results}
