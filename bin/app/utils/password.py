import hashlib

# Hardcoded salt (pepper)
PEPPER = "s3cr3tP3pp3r!"

def hash_password(password):
    """Hash a password using SHA-256 with a hardcoded salt (pepper)."""
    peppered_password = PEPPER + password
    hash_obj = hashlib.sha256(peppered_password.encode())  # Create a hash with pepper
    password_hash = hash_obj.hexdigest()
    return password_hash
