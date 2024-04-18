import json
from utils.logger import logger
from utils.db_operations import create_db_connection
from utils.password import hash_password

def user_exists(email: str, phone: str) -> bool:
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM USERS WHERE email = %s AND phone = %s",
                (email, phone)
            )
            result = cursor.fetchone()
            exists = result[0] > 0
            logger.debug(f"User exists check for {email}: {exists}")
            return exists
        except Exception as e:
            logger.error(f"Error checking if user exists for {email}: {e}")
        finally:
            cursor.close()
            connection.close()
    return False

def is_user_verified(email: str, phone: str) -> bool:
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT is_verified FROM USERS WHERE email = %s AND phone = %s",
                (email, phone)
            )
            result = cursor.fetchone()
            verified = result[0] if result else False
            logger.debug(f"Verification status for {email}: {verified}")
            return verified
        except Exception as e:
            logger.error(f"Error verifying user for {email}: {e}")
        finally:
            cursor.close()
            connection.close()
    return False

def get_user_data(email: str, phone: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT name, surname, password, is_verified, test_completed FROM USERS WHERE email = %s AND phone = %s",
                (email, phone)
            )
            result = cursor.fetchone()
            if result:
                data = {
                    'name': result[0],
                    'surname': result[1],
                    'password_hash': result[2],
                    'is_verified': result[3],
                    'test_completed': result[4]
                }
                logger.debug(f"User data retrieved for {email}: {data}")
                return data
        except Exception as e:
            logger.error(f"Error retrieving user data for {email}: {e}")
        finally:
            cursor.close()
            connection.close()
    return None


def mark_user_as_verified(email: str, phone: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE USERS SET is_verified = TRUE WHERE email = %s AND phone = %s",
                (email, phone)
            )
            connection.commit()
            logger.info(f"User {email} marked as verified.")
        except Exception as e:
            logger.error(f"Error marking user as verified for {email}: {e}")
        finally:
            cursor.close()
            connection.close()

def register_user(email: str, phone: str, name: str, surname: str, verification_code: str, hashed_password: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO USERS (email, phone, name, surname, verification_code, password) VALUES (%s, %s, %s, %s, %s, %s)",
                (email, phone, name, surname, verification_code, hashed_password)
            )
            connection.commit()
            logger.info(f"User {email} registered successfully.")
        except Exception as e:
            logger.error(f"Error registering user {email}: {e}")
        finally:
            cursor.close()
            connection.close()

def mark_test_as_completed(email: str, score: float, phone: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE USERS SET test_completed = TRUE, test_score = %s WHERE email = %s AND phone = %s",
                (score, email, phone)
            )
            connection.commit()
            logger.info(f"Test marked as completed for {email}. Score: {score}")
        except Exception as e:
            logger.error(f"Error marking test as completed for {email}: {e}")
        finally:
            cursor.close()
            connection.close()

def save_user_progress(email: str, last_question_completed: int, answers: dict, phone: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            answers_json = json.dumps(answers)
            cursor.execute(
                "UPDATE USERS SET last_question_completed = %s, answers = %s WHERE email = %s AND phone = %s",
                (last_question_completed, answers_json, email, phone)
            )
            connection.commit()
            logger.info(f"User {email}'s progress saved.")
        except Exception as e:
            logger.error(f"Error saving user progress for {email}: {e}")
        finally:
            cursor.close()
            connection.close()


def check_password(email: str, password: str) -> bool:
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM USERS WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                stored_hash = bytes(result[0]).decode('utf-8') if isinstance(result[0], bytearray) else result[0]
                provided_hash = hash_password(password)
                return provided_hash == stored_hash
            return False
        except Exception as e:
            logger.error(f"Error checking password for {email}: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
    return False
