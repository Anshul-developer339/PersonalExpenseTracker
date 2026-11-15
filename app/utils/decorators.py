from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def login_required(f):
    """Custom login required decorator with flash message"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
