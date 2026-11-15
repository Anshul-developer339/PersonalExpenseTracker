import pytest
from app import create_app
from app.extensions import db
from app.models.user import User


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
    """Create authenticated client"""
    # Register a test user
    client.post('/auth/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    
    # Login
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    return client


def test_register_valid(client):
    """Test user registration with valid data"""
    response = client.post('/auth/register', data={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Registration successful' in response.data


def test_register_duplicate_email(client):
    """Test registration with duplicate email"""
    # First registration
    client.post('/auth/register', data={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    
    # Second registration with same email
    response = client.post('/auth/register', data={
        'name': 'Jane Doe',
        'email': 'john@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    
    assert response.status_code == 200
    assert b'already registered' in response.data


def test_register_invalid_email(client):
    """Test registration with invalid email"""
    response = client.post('/auth/register', data={
        'name': 'John Doe',
        'email': 'invalid-email',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    
    assert response.status_code == 200
    assert b'Invalid email' in response.data


def test_register_password_mismatch(client):
    """Test registration with password mismatch"""
    response = client.post('/auth/register', data={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123',
        'confirm_password': 'different'
    })
    
    assert response.status_code == 200
    assert b'do not match' in response.data


def test_register_short_password(client):
    """Test registration with short password"""
    response = client.post('/auth/register', data={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': '123',
        'confirm_password': '123'
    })
    
    assert response.status_code == 200
    assert b'at least 6 characters' in response.data


def test_login_valid(client):
    """Test login with valid credentials"""
    # Register first
    client.post('/auth/register', data={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    
    # Login
    response = client.post('/auth/login', data={
        'email': 'john@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login successful' in response.data


def test_login_invalid_email(client):
    """Test login with invalid email"""
    response = client.post('/auth/login', data={
        'email': 'nonexistent@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_login_invalid_password(client):
    """Test login with invalid password"""
    # Register first
    client.post('/auth/register', data={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    
    # Login with wrong password
    response = client.post('/auth/login', data={
        'email': 'john@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_logout(auth_client):
    """Test logout functionality"""
    response = auth_client.get('/auth/logout', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'logged out' in response.data


def test_protected_route_redirect(client):
    """Test that protected routes redirect to login"""
    response = client.get('/dashboard/', follow_redirects=False)
    
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_authenticated_access_dashboard(auth_client):
    """Test that authenticated user can access dashboard"""
    response = auth_client.get('/dashboard/')
    
    assert response.status_code == 200
