from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.db_operations import create_db_connection
from utils.logger import logger
from utils.email_operations import send_invitation_email, send_rejection_email, update_email_status

async def resend_emails():
    conn = create_db_connection()
    if conn is None:
        logger.error("Failed to connect to database to resend emails.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT email, test_score, final_email_sent FROM USERS
            WHERE test_completed = TRUE AND is_verified = TRUE AND final_email_sent = FALSE
            """
        )
        users = cursor.fetchall()
        for email, test_score, final_email_sent in users:
            if final_email_sent:
                continue
            if test_score < 50:
                await send_rejection_email(email)
            else:
                await send_invitation_email(email)
            update_email_status(email, True)
            logger.info(f"Email based on test score sent to {email}. Test Score: {test_score}")

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
        scheduler.add_job(resend_emails, 'interval', minutes=15)
        scheduler.start()
        logger.info("Scheduler has been set up and started.")
    except Exception as e:
        logger.error(f"Error setting up or starting the scheduler: {e}")

if __name__ == "__main__":
    setup_scheduler()
