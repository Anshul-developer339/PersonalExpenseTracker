from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.budget_service import BudgetService
from app.utils.validators import validate_amount
from datetime import date

budgets_bp = Blueprint('budgets', __name__)

EXPENSE_CATEGORIES = ['Food', 'Shopping', 'Transportation', 'Education', 'Entertainment', 'Healthcare', 'Rent', 'Bills', 'Travel', 'Other']


@budgets_bp.route('/')
@login_required
def index():
    """Budget management page"""
    user_id = current_user.id
    today = date.today()
    
    # Get current month and year from query params or use current
    month = request.args.get('month', type=int) or today.month
    year = request.args.get('year', type=int) or today.year
    
    # Get budgets for the month
    budgets = BudgetService.get_user_budgets(user_id, month, year)
    
    # Calculate utilization for each budget
    budget_data = []
    for budget in budgets:
        utilization = BudgetService.get_budget_utilization(budget)
        budget_data.append({
            'budget': budget,
            'spent': utilization['spent'],
            'remaining': utilization['remaining'],
            'utilization': utilization['utilization']
        })
    
    return render_template('budgets/index.html',
                         budgets=budget_data,
                         categories=EXPENSE_CATEGORIES,
                         current_month=month,
                         current_year=year)


@budgets_bp.route('/add', methods=['POST'])
@login_required
def add():
    """Add new budget"""
    category = request.form.get('category')
    monthly_limit = request.form.get('monthly_limit')
    month = request.form.get('month', type=int)
    year = request.form.get('year', type=int)
    
    # Validation
    if not category:
        flash('Please select a category.', 'danger')
        return redirect(url_for('budgets.index', month=month, year=year))
    
    valid, result = validate_amount(monthly_limit)
    if not valid:
        flash(result, 'danger')
        return redirect(url_for('budgets.index', month=month, year=year))
    monthly_limit = result
    
    if not month or not year:
        flash('Invalid month or year.', 'danger')
        return redirect(url_for('budgets.index'))
    
    # Check if budget already exists
    from app.models.budget import Budget
    existing = Budget.query.filter_by(
        user_id=current_user.id,
        category=category,
        month=month,
        year=year
    ).first()
    
    if existing:
        flash('Budget for this category already exists for this month.', 'warning')
        return redirect(url_for('budgets.index', month=month, year=year))
    
    # Create budget
    BudgetService.create_budget(
        user_id=current_user.id,
        category=category,
        monthly_limit=monthly_limit,
        month=month,
        year=year
    )
    
    flash('Budget created successfully!', 'success')
    return redirect(url_for('budgets.index', month=month, year=year))


@budgets_bp.route('/edit/<int:budget_id>', methods=['POST'])
@login_required
def edit(budget_id):
    """Edit budget"""
    budget = BudgetService.get_budget_by_id(budget_id, current_user.id)
    
    if not budget:
        flash('Budget not found.', 'danger')
        return redirect(url_for('budgets.index'))
    
    category = request.form.get('category')
    monthly_limit = request.form.get('monthly_limit')
    
    # Validation
    if not category:
        flash('Please select a category.', 'danger')
        return redirect(url_for('budgets.index', month=budget.month, year=budget.year))
    
    valid, result = validate_amount(monthly_limit)
    if not valid:
        flash(result, 'danger')
        return redirect(url_for('budgets.index', month=budget.month, year=budget.year))
    monthly_limit = result
    
    # Check if category conflicts with another budget
    from app.models.budget import Budget
    existing = Budget.query.filter(
        Budget.user_id == current_user.id,
        Budget.category == category,
        Budget.month == budget.month,
        Budget.year == budget.year,
        Budget.id != budget_id
    ).first()
    
    if existing:
        flash('Budget for this category already exists for this month.', 'warning')
        return redirect(url_for('budgets.index', month=budget.month, year=budget.year))
    
    # Update budget
    BudgetService.update_budget(budget, category, monthly_limit)
    
    flash('Budget updated successfully!', 'success')
    return redirect(url_for('budgets.index', month=budget.month, year=budget.year))


@budgets_bp.route('/delete/<int:budget_id>', methods=['POST'])
@login_required
def delete(budget_id):
    """Delete budget"""
    budget = BudgetService.get_budget_by_id(budget_id, current_user.id)
    
    if not budget:
        flash('Budget not found.', 'danger')
        return redirect(url_for('budgets.index'))
    
    month, year = budget.month, budget.year
    BudgetService.delete_budget(budget)
    
    flash('Budget deleted successfully!', 'success')
    return redirect(url_for('budgets.index', month=month, year=year))
