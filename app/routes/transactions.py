from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.transaction import Transaction
from app.services.transaction_service import TransactionService
from app.utils.validators import validate_amount, validate_date
from datetime import date

transactions_bp = Blueprint('transactions', __name__)

INCOME_CATEGORIES = ['Salary', 'Freelancing', 'Business', 'Investment', 'Gift', 'Other']
EXPENSE_CATEGORIES = ['Food', 'Shopping', 'Transportation', 'Education', 'Entertainment', 'Healthcare', 'Rent', 'Bills', 'Travel', 'Other']


@transactions_bp.route('/')
@login_required
def index():
    """Transaction history page with filters"""
    user_id = current_user.id
    
    # Get filter parameters
    transaction_type = request.args.get('type')
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    search = request.args.get('search')
    
    # Build filters
    filters = {}
    if transaction_type:
        filters['type'] = transaction_type
    if category:
        filters['category'] = category
    if start_date:
        valid, result = validate_date(start_date)
        if valid:
            filters['start_date'] = result
    if end_date:
        valid, result = validate_date(end_date)
        if valid:
            filters['end_date'] = result
    if search:
        filters['search'] = search
    
    # Get transactions
    transactions = TransactionService.get_user_transactions(user_id, filters).all()
    
    return render_template('transactions/index.html',
                         transactions=transactions,
                         income_categories=INCOME_CATEGORIES,
                         expense_categories=EXPENSE_CATEGORIES,
                         current_type=transaction_type,
                         current_category=category,
                         current_start=start_date,
                         current_end=end_date,
                         current_search=search)


@transactions_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new transaction"""
    if request.method == 'POST':
        transaction_type = request.form.get('type')
        amount = request.form.get('amount')
        category = request.form.get('category')
        description = request.form.get('description', '').strip()
        transaction_date = request.form.get('transaction_date')
        
        # Validation
        if transaction_type not in ['income', 'expense']:
            flash('Invalid transaction type.', 'danger')
            return render_template('transactions/form.html',
                                 income_categories=INCOME_CATEGORIES,
                                 expense_categories=EXPENSE_CATEGORIES)
        
        valid, result = validate_amount(amount)
        if not valid:
            flash(result, 'danger')
            return render_template('transactions/form.html',
                                 income_categories=INCOME_CATEGORIES,
                                 expense_categories=EXPENSE_CATEGORIES)
        amount = result
        
        if not category:
            flash('Please select a category.', 'danger')
            return render_template('transactions/form.html',
                                 income_categories=INCOME_CATEGORIES,
                                 expense_categories=EXPENSE_CATEGORIES)
        
        valid, result = validate_date(transaction_date)
        if not valid:
            flash(result, 'danger')
            return render_template('transactions/form.html',
                                 income_categories=INCOME_CATEGORIES,
                                 expense_categories=EXPENSE_CATEGORIES)
        transaction_date = result
        
        # Create transaction
        TransactionService.create_transaction(
            user_id=current_user.id,
            type=transaction_type,
            amount=amount,
            category=category,
            description=description,
            transaction_date=transaction_date
        )
        
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions.index'))
    
    return render_template('transactions/form.html',
                         income_categories=INCOME_CATEGORIES,
                         expense_categories=EXPENSE_CATEGORIES)


@transactions_bp.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit(transaction_id):
    """Edit existing transaction"""
    transaction = TransactionService.get_transaction_by_id(transaction_id, current_user.id)
    
    if not transaction:
        flash('Transaction not found.', 'danger')
        return redirect(url_for('transactions.index'))
    
    if request.method == 'POST':
        transaction_type = request.form.get('type')
        amount = request.form.get('amount')
        category = request.form.get('category')
        description = request.form.get('description', '').strip()
        transaction_date = request.form.get('transaction_date')
        
        # Validation
        if transaction_type not in ['income', 'expense']:
            flash('Invalid transaction type.', 'danger')
            return render_template('transactions/form.html',
                                 transaction=transaction,
                                 income_categories=INCOME_CATEGORIES,
                                 expense_categories=EXPENSE_CATEGORIES,
                                 edit=True)
        
        valid, result = validate_amount(amount)
        if not valid:
            flash(result, 'danger')
            return render_template('transactions/form.html',
                                 transaction=transaction,
                                 income_categories=INCOME_CATEGORIES,
                                 expense_categories=EXPENSE_CATEGORIES,
                                 edit=True)
        amount = result
        
        if not category:
            flash('Please select a category.', 'danger')
            return render_template('transactions/form.html',
                                 transaction=transaction,
                                 income_categories=INCOME_CATEGORIES,
                                 expense_categories=EXPENSE_CATEGORIES,
                                 edit=True)
        
        valid, result = validate_date(transaction_date)
        if not valid:
            flash(result, 'danger')
            return render_template('transactions/form.html',
                                 transaction=transaction,
                                 income_categories=INCOME_CATEGORIES,
                                 expense_categories=EXPENSE_CATEGORIES,
                                 edit=True)
        transaction_date = result
        
        # Update transaction
        TransactionService.update_transaction(
            transaction=transaction,
            type=transaction_type,
            amount=amount,
            category=category,
            description=description,
            transaction_date=transaction_date
        )
        
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('transactions.index'))
    
    return render_template('transactions/form.html',
                         transaction=transaction,
                         income_categories=INCOME_CATEGORIES,
                         expense_categories=EXPENSE_CATEGORIES,
                         edit=True)


@transactions_bp.route('/delete/<int:transaction_id>', methods=['POST'])
@login_required
def delete(transaction_id):
    """Delete transaction"""
    transaction = TransactionService.get_transaction_by_id(transaction_id, current_user.id)
    
    if not transaction:
        flash('Transaction not found.', 'danger')
        return redirect(url_for('transactions.index'))
    
    TransactionService.delete_transaction(transaction)
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('transactions.index'))
