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
            logger.info(f"Verification code stored for {email}")
        except Exception as e:
            logger.error(f"Failed to store verification code for {email}: {e}")
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
            if result:
                logger.debug(f"Verification code retrieved for {email}: {result}")
            return result if result else (None, None)
        except Exception as e:
            logger.error(f"Failed to retrieve verification code for {email}: {e}")
            return None, None
        finally:
            cursor.close()
            connection.close()
    return None, None


def generate_verification_code():
    try:
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        logger.debug(f"Generated verification code: {code}")
        return code
    except Exception as e:
        logger.error(f"Failed to generate verification code: {e}")
        return None


def update_verification_code(email, new_code):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE USERS u
                INNER JOIN VERIFICATION_CODES vc ON u.email = vc.email
                SET u.verification_code = %s, vc.code = %s, vc.timestamp = %s
                WHERE u.email = %s
                """,
                (new_code, new_code, int(time.time()), email)
            )
            connection.commit()
            logger.info(f"Verification code updated for {email}")
        except Exception as e:
            logger.error(f"MySQL error: {e}")
            raise
        finally:
            cursor.close()
            connection.close()
