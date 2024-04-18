import hashlib
from utils.logger import logger
from utils.envs import SALT_PASSWORD

def hash_password(password: str) -> str:
    try:
        salt = ('SALT_PASSWORD')
        salted_password = salt + password
        hash_object = hashlib.sha256(salted_password.encode())
        hashed_password = hash_object.hexdigest()
        return hashed_password
    except Exception as e:
        logger.error(f'Error in hash_password() function: {e}')
