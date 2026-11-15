# Personal Expense Tracker

A full-stack web application for tracking personal finances, including income, expenses, budgets, and analytics.

## Project Introduction

This Personal Expense Tracker is a comprehensive financial management tool designed to help individuals monitor their income, expenses, and spending habits. The application provides a modern, user-friendly interface with powerful features for transaction management, budget tracking, and financial analytics.

## Problem Statement

Managing personal finances manually is time-consuming and error-prone. Many people struggle to:
- Track their daily expenses accurately
- Monitor spending patterns across different categories
- Stay within monthly budgets
- Understand their financial health through visual analytics

This application addresses these challenges by providing an automated, centralized platform for personal finance management.

## Objectives

- Enable users to register and securely manage their financial data
- Provide intuitive interfaces for adding, editing, and deleting transactions
- Offer budget management with real-time utilization tracking
- Deliver comprehensive analytics with visual charts
- Ensure data security and user privacy through proper authentication
- Create a responsive design accessible on various devices

## Technology Stack

### Frontend
- **HTML5** - Structure and semantics
- **CSS3** - Styling with custom CSS variables
- **JavaScript (Vanilla)** - Client-side interactivity
- **Bootstrap 5** - Responsive framework
- **Bootstrap Icons** - Iconography
- **Chart.js** - Data visualization

### Backend
- **Python 3** - Programming language
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-Login** - User authentication
- **Flask-WTF** - CSRF protection
- **Werkzeug** - Password hashing

### Database
- **SQLite** - Lightweight database (can be upgraded to PostgreSQL/MySQL)

### Additional
- **Jinja2** - Template engine
- **python-dotenv** - Environment variable management
- **pytest** - Testing framework

## Features

### Authentication
- User registration with email validation
- Secure login with password hashing
- Session management with remember me functionality
- Protected routes for authenticated users
- Logout functionality

### Dashboard
- Real-time financial summary cards (Income, Expenses, Balance, Savings)
- Monthly income vs expense chart
- Expense category breakdown (pie/doughnut chart)
- Recent transactions list
- Quick add transaction button

### Transaction Management
- Add income and expense transactions
- Edit existing transactions
- Delete transactions with confirmation
- Search transactions by description or category
- Filter by transaction type (income/expense)
- Filter by category
- Filter by date range
- Sort transactions
- CSV export of all transactions

### Budget Management
- Create monthly budgets for different categories
- Set spending limits per category
- Edit and delete budgets
- Real-time budget utilization tracking
- Progress bars with color-coded warnings
- Warnings at 75%, 90%, and 100% utilization
- Month/year navigation

### Analytics
- Monthly income and expense reports
- Category-wise expense breakdown
- Income vs expense comparison charts
- Monthly spending trends (line chart)
- Highest spending category identification
- Average monthly expenses calculation
- Year-wise data analysis
- CSV export functionality

### Profile/Settings
- Update user name and email
- View account information
- Member since date display

### Additional Features
- Responsive design for mobile, tablet, and desktop
- Modern, clean UI with consistent design system
- Error pages (404, 500)
- Flash messages for user feedback
- CSRF protection on all forms
- Data isolation between users

## Folder Structure

```
personal-expense-tracker/
│
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── extensions.py            # Flask extensions initialization
│   │
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   ├── transaction.py       # Transaction model
│   │   └── budget.py            # Budget model
│   │
│   ├── routes/                  # Application routes (Blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes
│   │   ├── dashboard.py         # Dashboard routes
│   │   ├── transactions.py      # Transaction routes
│   │   ├── budgets.py           # Budget routes
│   │   ├── analytics.py         # Analytics routes
│   │   ├── profile.py           # Profile routes
│   │   └── errors.py            # Error handlers
│   │
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── transaction_service.py
│   │   ├── budget_service.py
│   │   └── analytics_service.py
│   │
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py        # Input validation
│   │   └── decorators.py        # Custom decorators
│   │
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html            # Base template
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard/
│   │   │   └── index.html
│   │   ├── transactions/
│   │   │   ├── index.html
│   │   │   └── form.html
│   │   ├── budgets/
│   │   │   └── index.html
│   │   ├── analytics/
│   │   │   └── index.html
│   │   ├── profile/
│   │   │   └── index.html
│   │   └── errors/
│   │       ├── 404.html
│   │       └── 500.html
│   │
│   └── static/                  # Static assets
│       ├── css/
│       │   ├── style.css        # Main styles
│       │   ├── dashboard.css    # Dashboard-specific styles
│       │   └── responsive.css   # Responsive design
│       ├── js/
│       │   ├── main.js          # Global JavaScript
│       │   ├── dashboard.js     # Dashboard functionality
│       │   ├── transactions.js  # Transaction functionality
│       │   ├── budgets.js       # Budget functionality
│       │   └── analytics.js     # Analytics functionality
│       └── images/
│
├── migrations/                  # Database migrations (if using Flask-Migrate)
├── tests/                       # Automated tests
│   ├── test_auth.py
│   ├── test_transactions.py
│   ├── test_budgets.py
│   └── test_dashboard.py
│
├── instance/                    # Instance folder (SQLite database)
│   └── .gitkeep
│
├── config.py                    # Application configuration
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
└── PROJECT_DOCUMENTATION.md     # Detailed project documentation
```

## Database Schema

### Users Table
- `id` - Primary key
- `name` - User's full name
- `email` - Unique email address
- `password_hash` - Hashed password
- `created_at` - Account creation timestamp

### Transactions Table
- `id` - Primary key
- `user_id` - Foreign key to Users
- `type` - Transaction type (income/expense)
- `amount` - Transaction amount
- `category` - Transaction category
- `description` - Transaction description
- `transaction_date` - Date of transaction
- `created_at` - Record creation timestamp

### Budgets Table
- `id` - Primary key
- `user_id` - Foreign key to Users
- `category` - Budget category
- `monthly_limit` - Monthly spending limit
- `month` - Month (1-12)
- `year` - Year
- `created_at` - Record creation timestamp

**Unique Constraint**: No duplicate budgets for same user, category, month, and year.

## Installation Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Windows PowerShell Setup

1. **Navigate to the project directory**
   ```powershell
   cd C:\Users\solol\CascadeProjects\personal-expense-tracker
   ```

2. **Create a virtual environment**
   ```powershell
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```powershell
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Create environment file**
   ```powershell
   copy .env.example .env
   ```
   
   Edit `.env` file and set your preferred values (optional for development).

6. **Run the application**
   ```powershell
   python run.py
   ```

7. **Open in browser**
   Navigate to: http://127.0.0.1:5000

### Linux/Mac Setup

1. **Navigate to the project directory**
   ```bash
   cd personal-expense-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment file**
   ```bash
   cp .env.example .env
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Open in browser**
   Navigate to: http://127.0.0.1:5000

## How to Run the Application

1. Ensure the virtual environment is activated
2. Ensure all dependencies are installed
3. Run `python run.py`
4. Open http://127.0.0.1:5000 in your web browser
5. Register a new account
6. Login and start tracking your expenses

## Test Execution Instructions

### Running All Tests
```powershell
pytest
```

### Running Specific Test File
```powershell
pytest tests/test_auth.py
```

### Running with Verbose Output
```powershell
pytest -v
```

### Running with Coverage Report
```powershell
pytest --cov=app --cov-report=html
```

## Screenshots Section

*Note: Screenshots will be added after running the application and capturing the UI.*

### Dashboard
- Summary cards showing total income, expenses, balance, and savings
- Monthly income vs expense chart
- Category-wise expense breakdown
- Recent transactions table

### Transactions
- Transaction list with filters
- Add/Edit transaction form
- Search and filter functionality

### Budgets
- Budget cards with progress bars
- Utilization warnings
- Month/year navigation

### Analytics
- Monthly trend charts
- Category spending analysis
- Export options

## Team Development

This project is designed for collaborative development by two team members:

### Member 1: Ansh
**Responsibilities:**
- Frontend development
- UI/UX design
- HTML/CSS
- JavaScript
- Dashboard
- Charts
- Responsive design

### Member 2: Anshul
**Responsibilities:**
- Flask backend
- Database architecture
- Authentication
- Transaction management
- Budget logic
- Analytics calculations
- Testing

### Recommended Git Workflow

1. **Create branches for features**
   ```bash
   git checkout -b feature/dashboard
   git checkout -b feature/authentication
   ```

2. **Commit frequently with descriptive messages**
   ```bash
   git add .
   git commit -m "Add user registration functionality"
   ```

3. **Push to remote repository**
   ```bash
   git push origin feature/dashboard
   ```

4. **Create pull requests for review**
   - Review each other's code before merging
   - Ensure tests pass
   - Document any breaking changes

5. **Merge to main branch**
   ```bash
   git checkout main
   git merge feature/dashboard
   ```

## Future Scope

### Planned Enhancements
- PDF report generation
- Recurring transactions
- Transaction categories customization
- Multi-currency support
- Data import from CSV
- Mobile app (React Native/Flutter)
- Dark mode theme
- Email notifications for budget alerts
- Data export in multiple formats (JSON, PDF)
- Advanced analytics with predictions
- Goal setting and tracking
- Investment tracking
- Bank account integration
- Receipt image upload
- Tags for transactions
- Sub-categories
- Budget rollover to next month
- Shared budgets for families
- API for third-party integrations

### Performance Improvements
- Database indexing optimization
- Caching layer (Redis)
- Pagination for large datasets
- Lazy loading for charts
- Database query optimization

### Security Enhancements
- Two-factor authentication
- Password strength requirements
- Account lockout after failed attempts
- Audit logging
- Data encryption at rest

## Troubleshooting

### Common Issues

**Issue: Database not created**
- Solution: The database is automatically created on first run. Ensure the `instance` folder exists.

**Issue: Import errors**
- Solution: Ensure virtual environment is activated and dependencies are installed.

**Issue: Port already in use**
- Solution: Change the port in `run.py` or stop the process using port 5000.

**Issue: Tests failing**
- Solution: Ensure you're using the testing configuration and the test database is properly initialized.

## License

This project is created for educational purposes.

## Contact

For questions or issues, please contact the development team.

---

**Version:** 1.0.0  
**Last Updated:** November 2024
