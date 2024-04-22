from utils.db_operations import create_db_connection
from utils.logger import logger
from utils.phone_operations import ZadarmaAPI
from utils.envs import ZADARMA_API_KEY, ZADARMA_API_SECRET


api = ZadarmaAPI(ZADARMA_API_KEY, ZADARMA_API_SECRET)

async def resend_messages():
    connection = create_db_connection()
    if connection is None:
        logger.error("Failed to connect to database to resend emails.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT phone, test_score, lang, final_message_sent FROM USERS
            WHERE test_completed = TRUE AND is_verified = TRUE AND final_message_sent = FALSE
            """
        )
        users = cursor.fetchall()
        for phone, test_score, lang, final_message_sent in users:
            if final_message_sent:
                continue
            if test_score < 50:
                api.send_rejection_message(phone, lang)
            else:
                api.send_invitation_message(phone, lang)
            logger.info(f"Email based on test score sent to {phone}. Test Score: {test_score}")

    except Exception as e:
        logger.error(f"Error in the email resending process: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
