import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.budget import Budget


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def auth_client(client):
    """Create authenticated client with test user"""
    client.post('/auth/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    return client


def test_add_budget(auth_client):
    """Test adding a budget"""
    response = auth_client.post('/budgets/add', data={
        'category': 'Food',
        'monthly_limit': '5000',
        'month': '1',
        'year': '2024'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Budget created successfully' in response.data


def test_add_duplicate_budget(auth_client):
    """Test adding duplicate budget for same category/month/year"""
    # Add first budget
    auth_client.post('/budgets/add', data={
        'category': 'Food',
        'monthly_limit': '5000',
        'month': '1',
        'year': '2024'
    })
    
    # Try to add duplicate
    response = auth_client.post('/budgets/add', data={
        'category': 'Food',
        'monthly_limit': '6000',
        'month': '1',
        'year': '2024'
    })
    
    assert response.status_code == 200
    assert b'already exists' in response.data


def test_add_invalid_amount(auth_client):
    """Test adding budget with invalid amount"""
    response = auth_client.post('/budgets/add', data={
        'category': 'Food',
        'monthly_limit': '-100',
        'month': '1',
        'year': '2024'
    })
    
    assert response.status_code == 200
    assert b'greater than zero' in response.data


def test_view_budgets(auth_client):
    """Test viewing budgets list"""
    # Add a budget
    auth_client.post('/budgets/add', data={
        'category': 'Food',
        'monthly_limit': '5000',
        'month': '1',
        'year': '2024'
    })
    
    response = auth_client.get('/budgets/?month=1&year=2024')
    
    assert response.status_code == 200
    assert b'Food' in response.data


def test_edit_budget(auth_client):
    """Test editing a budget"""
    # Add a budget
    auth_client.post('/budgets/add', data={
        'category': 'Food',
        'monthly_limit': '5000',
        'month': '1',
        'year': '2024'
    })
    
    # Get budget ID
    with auth_client.application.app_context():
        budget = Budget.query.filter_by(user_id=1).first()
        budget_id = budget.id
    
    # Edit budget
    response = auth_client.post(f'/budgets/edit/{budget_id}', data={
        'category': 'Food',
        'monthly_limit': '6000'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Budget updated successfully' in response.data


def test_delete_budget(auth_client):
    """Test deleting a budget"""
    # Add a budget
    auth_client.post('/budgets/add', data={
        'category': 'Food',
        'monthly_limit': '5000',
        'month': '1',
        'year': '2024'
    })
    
    # Get budget ID
    with auth_client.application.app_context():
        budget = Budget.query.filter_by(user_id=1).first()
        budget_id = budget.id
    
    # Delete budget
    response = auth_client.post(f'/budgets/delete/{budget_id}', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Budget deleted successfully' in response.data


def test_budget_utilization(auth_client):
    """Test budget utilization calculation"""
    # Add budget
    auth_client.post('/budgets/add', data={
        'category': 'Food',
        'monthly_limit': '5000',
        'month': '1',
        'year': '2024'
    })
    
    # Add expense
    auth_client.post('/transactions/add', data={
        'type': 'expense',
        'amount': '3500',
        'category': 'Food',
        'transaction_date': '2024-01-15'
    })
    
    response = auth_client.get('/budgets/?month=1&year=2024')
    
    assert response.status_code == 200
    assert b'70%' in response.data or b'3500' in response.data
