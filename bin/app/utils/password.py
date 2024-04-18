import hashlib

from utils.envs import SALT_PASSWORD
def hash_password(password: str) -> str:
    salt = ('SALT_PASSWORD')
    salted_password = salt + password
    hash_object = hashlib.sha256(salted_password.encode())
    hashed_password = hash_object.hexdigest()
    return hashed_password
