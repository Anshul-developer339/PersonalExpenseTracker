import pytest
from datetime import date
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
    # Register and login
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


def test_add_income(auth_client):
    """Test adding income transaction"""
    response = auth_client.post('/transactions/add', data={
        'type': 'income',
        'amount': '5000',
        'category': 'Salary',
        'description': 'Monthly salary',
        'transaction_date': '2024-01-15'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Transaction added successfully' in response.data


def test_add_expense(auth_client):
    """Test adding expense transaction"""
    response = auth_client.post('/transactions/add', data={
        'type': 'expense',
        'amount': '500',
        'category': 'Food',
        'description': 'Groceries',
        'transaction_date': '2024-01-15'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Transaction added successfully' in response.data


def test_add_invalid_amount(auth_client):
    """Test adding transaction with invalid amount"""
    response = auth_client.post('/transactions/add', data={
        'type': 'income',
        'amount': '-100',
        'category': 'Salary',
        'transaction_date': '2024-01-15'
    })
    
    assert response.status_code == 200
    assert b'greater than zero' in response.data


def test_add_invalid_date(auth_client):
    """Test adding transaction with invalid date"""
    response = auth_client.post('/transactions/add', data={
        'type': 'income',
        'amount': '5000',
        'category': 'Salary',
        'transaction_date': 'invalid-date'
    })
    
    assert response.status_code == 200
    assert b'Invalid date' in response.data


def test_view_transactions(auth_client):
    """Test viewing transactions list"""
    # Add a transaction first
    auth_client.post('/transactions/add', data={
        'type': 'income',
        'amount': '5000',
        'category': 'Salary',
        'transaction_date': '2024-01-15'
    })
    
    response = auth_client.get('/transactions/')
    
    assert response.status_code == 200
    assert b'Salary' in response.data


def test_filter_by_type(auth_client):
    """Test filtering transactions by type"""
    # Add income and expense
    auth_client.post('/transactions/add', data={
        'type': 'income',
        'amount': '5000',
        'category': 'Salary',
        'transaction_date': '2024-01-15'
    })
    
    auth_client.post('/transactions/add', data={
        'type': 'expense',
        'amount': '500',
        'category': 'Food',
        'transaction_date': '2024-01-15'
    })
    
    # Filter by income
    response = auth_client.get('/transactions/?type=income')
    
    assert response.status_code == 200
    assert b'Salary' in response.data


def test_edit_transaction(auth_client):
    """Test editing a transaction"""
    # Add a transaction
    auth_client.post('/transactions/add', data={
        'type': 'income',
        'amount': '5000',
        'category': 'Salary',
        'transaction_date': '2024-01-15'
    })
    
    # Get transaction ID
    with auth_client.application.app_context():
        transaction = Transaction.query.filter_by(user_id=1).first()
        transaction_id = transaction.id
    
    # Edit transaction
    response = auth_client.post(f'/transactions/edit/{transaction_id}', data={
        'type': 'income',
        'amount': '6000',
        'category': 'Salary',
        'transaction_date': '2024-01-15'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Transaction updated successfully' in response.data


def test_delete_transaction(auth_client):
    """Test deleting a transaction"""
    # Add a transaction
    auth_client.post('/transactions/add', data={
        'type': 'income',
        'amount': '5000',
        'category': 'Salary',
        'transaction_date': '2024-01-15'
    })
    
    # Get transaction ID
    with auth_client.application.app_context():
        transaction = Transaction.query.filter_by(user_id=1).first()
        transaction_id = transaction.id
    
    # Delete transaction
    response = auth_client.post(f'/transactions/delete/{transaction_id}', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Transaction deleted successfully' in response.data


def test_user_data_isolation(client):
    """Test that users cannot see each other's transactions"""
    # Create first user and add transaction
    client.post('/auth/register', data={
        'name': 'User 1',
        'email': 'user1@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    client.post('/auth/login', data={
        'email': 'user1@example.com',
        'password': 'password123'
    })
    client.post('/transactions/add', data={
        'type': 'income',
        'amount': '5000',
        'category': 'Salary',
        'transaction_date': '2024-01-15'
    })
    client.get('/auth/logout')
    
    # Create second user
    client.post('/auth/register', data={
        'name': 'User 2',
        'email': 'user2@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    client.post('/auth/login', data={
        'email': 'user2@example.com',
        'password': 'password123'
    })
    
    # Second user should not see first user's transactions
    response = client.get('/transactions/')
    
    assert response.status_code == 200
    assert b'Salary' not in response.data
