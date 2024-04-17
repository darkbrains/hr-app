import asyncio
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.logger import logger
from utils.envs import EMAIL_ADDRESS, EMAIL_PASSWORD
from utils.db_operations import create_db_connection

def send_email(receiver_email, code):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Verification Code"
        message["From"] = EMAIL_ADDRESS
        message["To"] = receiver_email
        text = f"Your verification code is: {code}. This code will expire in 5 minutes."
        part1 = MIMEText(text, "plain")
        message.attach(part1)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, receiver_email, message.as_string())
            logger.info(f"Verification email sent to {receiver_email}")

    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred while sending email to {receiver_email}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred while sending email to {receiver_email}: {e}")

def update_email_status(email, status):
    conn = create_db_connection()
    if conn is None:  # Correcting the condition to check for a None value
        logger.error("Failed to connect to database for updating email status.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE USERS SET final_email_sent = %s WHERE email = %s",
            (status, email)
        )
        conn.commit()
        logger.info(f"Email sent status updated to {status} for {email}")
    except Exception as e:
        logger.error(f"Error updating email status for {email}: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def send_custom_email(receiver_email, subject, message):
    try:
        mime_message = MIMEMultipart("alternative")
        mime_message["Subject"] = subject
        mime_message["From"] = EMAIL_ADDRESS
        mime_message["To"] = receiver_email
        part1 = MIMEText(message, "plain")
        mime_message.attach(part1)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, receiver_email, mime_message.as_string())
            logger.info(f"Custom email sent to {receiver_email}")

    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred while sending email to {receiver_email}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred while sending email to {receiver_email}: {e}")

async def send_email_with_delay(email, score):
    if score < 50:
        await send_rejection_email(email)
    else:
        await send_invitation_email(email)

async def send_rejection_email(receiver_email):
    subject = "Thank You for Your Participation"
    message = (
        "Thank you for your time and patience throughout the interview process.\n\n"
        "We regret to inform you that your result did not qualify for the next stage of the recruitment process.\n\n"
        "We wish you all the best in your future endeavors.\n\n"
        "Best regards,\nThe People Connect Team"
    )
    await asyncio.sleep(60)  # Simulating a delay
    send_custom_email(receiver_email, subject, message)
    logger.info(f"Rejection email sent to {receiver_email}")
    update_email_status(receiver_email, True)

async def send_invitation_email(receiver_email):
    subject = "Congratulations - Next Steps in People Connect"
    message = (
        "Congratulations on successfully passing the initial screening!\n\n"
        "We are pleased to invite you to the next interview stage for a specific position with our company.\n\n"
        "We will notify you of further actions within 2 business days.\n\n"
        "Best regards,\nThe People Connect Team"
    )
    await asyncio.sleep(60)  # Simulating a delay
    send_custom_email(receiver_email, subject, message)
    logger.info(f"Invitation email sent to {receiver_email}")
    update_email_status(receiver_email, True)
