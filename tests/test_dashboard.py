import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.transaction import Transaction


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


def test_dashboard_access(auth_client):
    """Test that authenticated user can access dashboard"""
    response = auth_client.get('/dashboard/')
    
    assert response.status_code == 200
    assert b'Dashboard' in response.data


def test_dashboard_calculations(auth_client):
    """Test dashboard financial calculations"""
    # Add income
    auth_client.post('/transactions/add', data={
        'type': 'income',
        'amount': '10000',
        'category': 'Salary',
        'transaction_date': '2024-01-15'
    })
    
    # Add expense
    auth_client.post('/transactions/add', data={
        'type': 'expense',
        'amount': '3000',
        'category': 'Food',
        'transaction_date': '2024-01-15'
    })
    
    response = auth_client.get('/dashboard/')
    
    assert response.status_code == 200
    assert b'10,000' in response.data or b'10000' in response.data
    assert b'3,000' in response.data or b'3000' in response.data


def test_dashboard_recent_transactions(auth_client):
    """Test dashboard shows recent transactions"""
    # Add transactions
    auth_client.post('/transactions/add', data={
        'type': 'income',
        'amount': '5000',
        'category': 'Salary',
        'transaction_date': '2024-01-15'
    })
    
    response = auth_client.get('/dashboard/')
    
    assert response.status_code == 200
    assert b'Recent Transactions' in response.data


def test_dashboard_empty_state(auth_client):
    """Test dashboard with no transactions"""
    response = auth_client.get('/dashboard/')
    
    assert response.status_code == 200
    assert b'No transactions yet' in response.data


def test_dashboard_redirect_unauthenticated(client):
    """Test that unauthenticated user is redirected from dashboard"""
    response = client.get('/dashboard/', follow_redirects=False)
    
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_csv_export(auth_client):
    """Test CSV export functionality"""
    # Add a transaction
    auth_client.post('/transactions/add', data={
        'type': 'income',
        'amount': '5000',
        'category': 'Salary',
        'transaction_date': '2024-01-15'
    })
    
    response = auth_client.get('/analytics/export/csv')
    
    assert response.status_code == 200
    assert b'text/csv' in response.data
    assert b'Salary' in response.data
