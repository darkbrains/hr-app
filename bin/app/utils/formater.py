from utils.logger import logger

def format_name(name: str) -> str:
    if name is None:
        return None
    """Capitalize only the first letter of the name, others are lowercase."""
    try:
        formatted_name = name.strip().capitalize()
        logger.debug(f"Formatted name: {formatted_name}")
        return formatted_name
    except Exception as e:
        logger.error(f"Error formatting name: {e}")
        raise ValueError(f"Invalid input for name formatting: {name}")

def ensure_phone_format(phone: str) -> str:
    """Ensure the phone number starts with a + and contains only digits afterwards."""
    try:
        phone = phone.strip()
        if not phone.startswith('+'):
            phone = '+' + phone
        logger.debug(f"Formatted phone number: {phone}")
        return phone
    except Exception as e:
        logger.error(f"Error formatting phone number: {e}")
        raise ValueError(f"Invalid input for phone number formatting: {phone}")

def format_email(email: str) -> str:
    """Convert email to all lowercase."""
    try:
        formatted_email = email.strip().lower()
        logger.debug(f"Formatted email: {formatted_email}")
        return formatted_email
    except Exception as e:
        logger.error(f"Error formatting email: {e}")
        raise ValueError(f"Invalid input for email formatting: {email}")
