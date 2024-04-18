import mysql.connector
from mysql.connector import Error
from utils.logger import logger
from utils.envs import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT

def create_database_and_tables():
    host = DATABASE_HOST
    user = DATABASE_USER
    passwd = DATABASE_PASSWORD
    database = DATABASE_NAME
    port = DATABASE_PORT

    try:
        conn = mysql.connector.connect(host=host, user=user, passwd=passwd, port=port)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            logger.info(f"Database '{database}' created or already exists.")
            conn.database = database

            table_queries = [
                """
                CREATE TABLE IF NOT EXISTS USERS (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    phone VARCHAR(15) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    surname VARCHAR(255) NOT NULL,
                    verification_code VARCHAR(6) DEFAULT NULL,
                    password VARCHAR(255) DEFAULT NULL,
                    test_completed BOOLEAN DEFAULT FALSE,
                    last_question_completed INT DEFAULT 0,
                    answers JSON DEFAULT NULL,
                    is_verified BOOLEAN DEFAULT FALSE,
                    test_score FLOAT DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    final_email_sent BOOLEAN DEFAULT FALSE,
                    UNIQUE(email, phone),
                    INDEX(email),
                    INDEX(phone)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS VERIFICATION_CODES (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    code VARCHAR(6) NOT NULL,
                    timestamp INT NOT NULL,
                    INDEX(email),
                    FOREIGN KEY (email) REFERENCES USERS(email) ON DELETE CASCADE
                )
                """
            ]

            for query in table_queries:
                cursor.execute(query)
            cursor.close()
            conn.close()
            logger.info("Database tables are created successfully.")
    except Error as e:
        logger.error(f"Error while connecting to MySQL: {e}")


def create_db_connection():
    try:
        return mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            passwd=DATABASE_PASSWORD,
            database=DATABASE_NAME,
            port=DATABASE_PORT
        )
    except Error as e:
        logger.error(f"Error connecting to MySQL database: {e}")
        return None

def check_db_health():
    try:
        """Check the health of the database connection."""
        connection = create_db_connection()
        if connection and connection.is_connected():
            connection.close()
            return True
        return False
    except Error as e:
        logger.error(f"Error in check_db_health(): {e}")
