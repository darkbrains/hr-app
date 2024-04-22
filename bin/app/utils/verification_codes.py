import random
import time
from utils.logger import logger
from utils.db_operations import create_db_connection


def store_verification_code(email: str, email_code: str, phone_code: str):
    current_time = int(time.time())
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO VERIFICATION_CODES (email, email_code, phone_code, timestamp) VALUES (%s, %s, %s, %s)",
                (email, email_code, phone_code, current_time)
            )
            connection.commit()
            logger.info(f"Verification codes stored for {email}")
        except Exception as e:
            logger.error(f"Failed to store verification codes for {email}: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()


def get_verification_code(email: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT email_code, phone_code, timestamp FROM VERIFICATION_CODES WHERE email = %s ORDER BY timestamp DESC LIMIT 1",
                (email,)
            )
            result = cursor.fetchone()
            if result:
                logger.debug(f"Verification codes retrieved for {email}: {result}")
                return result
            else:
                return (None, None, None)
        except Exception as e:
            logger.error(f"Failed to retrieve verification codes for {email}: {e}")
            return (None, None, None)
        finally:
            cursor.close()
            connection.close()
    return (None, None, None)



def generate_verification_code():
    try:
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        logger.debug(f"Generated verification code: {code}")
        return code
    except Exception as e:
        logger.error(f"Failed to generate verification code: {e}")
        return None


def update_verification_code(email: str, new_email_code: str, new_phone_code: str = None):
    connection = create_db_connection()
    current_time = int(time.time())
    if connection:
        try:
            cursor = connection.cursor()
            if new_phone_code:
                cursor.execute(
                    """
                    UPDATE USERS u
                    INNER JOIN VERIFICATION_CODES vc ON u.email = vc.email
                    SET u.email_verification_code = %s,
                        u.phone_verification_code = %s,
                        vc.email_code = %s,
                        vc.phone_code = %s,
                        vc.timestamp = %s
                    WHERE u.email = %s
                    """,
                    (new_email_code, new_phone_code, new_email_code, new_phone_code, current_time, email)
                )
            else:
                cursor.execute(
                    """
                    UPDATE USERS u
                    INNER JOIN VERIFICATION_CODES vc ON u.email = vc.email
                    SET u.email_verification_code = %s,
                        vc.email_code = %s,
                        vc.timestamp = %s
                    WHERE u.email = %s
                    """,
                    (new_email_code, new_email_code, current_time, email)
                )
            connection.commit()
            logger.info(f"Updated verification codes for {email} in USERS and VERIFICATION_CODES.")
        except Exception as e:
            logger.error(f"Failed to update verification codes for {email}: {e}")
        finally:
            cursor.close()
            connection.close()
