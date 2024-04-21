from utils.db_operations import create_db_connection
from utils.logger import logger
from utils.email_operations import send_invitation_email, send_rejection_email, update_email_status

async def resend_emails():
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database to resend emails.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT email, test_score, lang, final_email_sent FROM USERS
            WHERE test_completed = TRUE AND is_verified = TRUE AND final_email_sent = FALSE
            """
        )
        users = cursor.fetchall()
        for email, test_score, lang, final_email_sent in users:
            if final_email_sent:
                continue
            if test_score < 50:
                send_rejection_email(email, lang)
            else:
                send_invitation_email(email, lang)
            update_email_status(email, True)
            logger.info(f"Email based on test score sent to {email}. Test Score: {test_score}")

    except Exception as e:
        logger.error(f"Error in the email resending process: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
