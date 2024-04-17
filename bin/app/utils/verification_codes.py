
import random
import time
from utils.logger import logger
from utils.db_operations import create_db_connection

def store_verification_code(email: str, code: str):
    current_time = int(time.time())
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO VERIFICATION_CODES (email, code, timestamp) VALUES (%s, %s, %s)",
                (email, code, current_time)
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

def get_verification_code(email: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT code, timestamp FROM VERIFICATION_CODES WHERE email = %s ORDER BY timestamp DESC LIMIT 1",
                (email,)
            )
            result = cursor.fetchone()
            return result if result else (None, None)
        finally:
            cursor.close()
            connection.close()
    return None, None

def generate_verification_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])
