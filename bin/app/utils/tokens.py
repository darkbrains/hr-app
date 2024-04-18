import secrets
from utils.logger import logger

tokens = {}

def generate_token(email, phone):
    """Generate a secure token and store it with the user's email and phone as a reference."""
    try:
        token = secrets.token_urlsafe()
        tokens[token] = {'email': email, 'phone': phone}
        return token
    except Exception as e:
        logger.error(f"Error generating token for {email}: {e}")
        return None

def get_user_data_from_token(token):
    """Retrieve the email and phone associated with a given token."""
    try:
        return tokens.get(token)
    except KeyError:
        logger.error("Token not found.")
        return None
    except Exception as e:
        logger.error(f"Error retrieving data for token: {e}")
        return None

def invalidate_token(token):
    """Invalidate a token when it's no longer needed or when the user logs out."""
    try:
        if token in tokens:
            del tokens[token]
    except KeyError:
        logger.error("Attempted to invalidate a non-existing token.")
    except Exception as e:
        logger.error(f"Error invalidating token: {e}")
