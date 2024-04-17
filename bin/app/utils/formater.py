def format_name(name: str) -> str:
    """Capitalize only the first letter of the name, others are lowercase."""
    return name.strip().capitalize()

def ensure_phone_format(phone: str) -> str:
    """Ensure the phone number starts with a + and contains only digits afterwards."""
    phone = phone.strip()
    if not phone.startswith('+'):
        phone = '+' + phone
    return phone

def format_email(email: str) -> str:
    """Convert email to all lowercase."""
    return email.strip().lower()
