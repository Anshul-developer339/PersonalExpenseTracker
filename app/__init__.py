from flask import Flask
from config import config
from app.extensions import db, login_manager, csrf
import os


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.transactions import transactions_bp
    from app.routes.budgets import budgets_bp
    from app.routes.analytics import analytics_bp
    from app.routes.profile import profile_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(budgets_bp, url_prefix='/budgets')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    
    # Register error handlers
    from app.routes.errors import errors_bp
    app.register_blueprint(errors_bp)
    
    # Root route
    from flask_login import current_user
    
    @app.route('/')
    def index():
        """Root route - redirect based on authentication status"""
        if current_user.is_authenticated:
            from flask import redirect, url_for
            return redirect(url_for('dashboard.index'))
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # User loader for Flask-Login
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app
