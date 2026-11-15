from datetime import datetime


def validate_amount(amount):
    """Validate that amount is a positive number"""
    try:
        amount_float = float(amount)
        if amount_float <= 0:
            return False, "Amount must be greater than zero"
        return True, amount_float
    except (ValueError, TypeError):
        return False, "Invalid amount format"


def validate_date(date_str):
    """Validate date string and return datetime object"""
    try:
        if isinstance(date_str, str):
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date_obj = date_str
        return True, date_obj
    except (ValueError, TypeError, AttributeError):
        return False, "Invalid date format. Use YYYY-MM-DD"


def validate_email(email):
    """Basic email validation"""
    if not email or '@' not in email or '.' not in email:
        return False, "Invalid email address"
    return True, email.lower()
