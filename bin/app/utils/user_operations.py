import json
from utils.logger import logger
from utils.db_operations import create_db_connection


def user_exists(email: str, phone: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM USERS WHERE email = %s AND phone = %s",
                (email, phone)
            )
            result = cursor.fetchone()
            return result[0] > 0
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
            return result[0] if result else False
        finally:
            cursor.close()
            connection.close()
    return False

def get_user_progress(email: str, phone: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT last_question_completed, answers, test_completed FROM USERS WHERE email = %s AND phone = %s",
                (email, phone)
            )
            result = cursor.fetchone()
            if result:
                print(f"User {email} progress retrieved: {result}")
                return {
                    'last_question_completed': result[0],
                    'answers': json.loads(result[1]) if result[1] else {},
                    'test_completed': result[2]
                }
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
        finally:
            cursor.close()
            connection.close()

def register_user(email: str, phone: str, name: str, surname: str, verification_code: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO USERS (email, phone, name, surname, verification_code) VALUES (%s, %s, %s, %s, %s)",
                (email, phone, name, surname, verification_code)
            )
            connection.commit()
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
                (int(score), email, phone)
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

def save_user_progress(email: str, last_question_completed: int, answers, phone: str):
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
        finally:
            cursor.close()
            connection.close()

def get_user_data(email: str, phone: str):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT name, surname FROM USERS WHERE email = %s AND phone = %s",
                (email, phone)
            )
            result = cursor.fetchone()
            if result:
                return {'name': result[0], 'surname': result[1]}
        finally:
            cursor.close()
            connection.close()
    return None
