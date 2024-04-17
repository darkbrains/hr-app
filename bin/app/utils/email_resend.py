from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.db_operations import create_db_connection
from utils.logger import logger
from utils.email_operations import send_custom_email, update_email_status
async def resend_emails():
    conn = create_db_connection()
    if conn is None:
        logger.error("Failed to connect to database to resend emails.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT email, subject, message FROM USERS
            WHERE test_completed = TRUE AND is_verified = TRUE AND final_email_sent = FALSE
            """
        )
        users = cursor.fetchall()
        for email, subject, message in users:
            await send_custom_email(email, subject, message)
            update_email_status(email, True)
            logger.info(f"Resent email to {email}: {subject}")

    except Exception as e:
        logger.error(f"Error in the email resending process: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def setup_scheduler():
    try:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(resend_emails, 'interval', minutes=5)
        scheduler.start()
        logger.info("Scheduler has been set up and started.")
    except Exception as e:
        logger.error(f"Failed to set up or start the scheduler: {e}")
