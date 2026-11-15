from datetime import datetime
from app.extensions import db


class Budget(db.Model):
    """Budget model for monthly spending limits"""
    __tablename__ = 'budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False)
    monthly_limit = db.Column(db.Float, nullable=False)
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate budgets
    __table_args__ = (
        db.UniqueConstraint('user_id', 'category', 'month', 'year', name='unique_user_category_month_year'),
    )
    
    def __repr__(self):
        return f'<Budget {self.category} - {self.month}/{self.year}>'
