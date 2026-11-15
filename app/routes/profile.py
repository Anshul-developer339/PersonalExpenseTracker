from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User
from app.extensions import db

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/')
@login_required
def index():
    """Profile settings page"""
    return render_template('profile/index.html')


@profile_bp.route('/update', methods=['POST'])
@login_required
def update():
    """Update user profile"""
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    
    # Validation
    if not name or len(name) < 2:
        flash('Name must be at least 2 characters.', 'danger')
        return redirect(url_for('profile.index'))
    
    if not email or '@' not in email:
        flash('Invalid email address.', 'danger')
        return redirect(url_for('profile.index'))
    
    email = email.lower()
    
    # Check if email is taken by another user
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.id != current_user.id:
        flash('Email already in use by another account.', 'danger')
        return redirect(url_for('profile.index'))
    
    # Update user
    current_user.name = name
    current_user.email = email
    db.session.commit()
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile.index'))
