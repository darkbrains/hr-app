import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.logger import logger
from utils.envs import EMAIL_ADDRESS, EMAIL_PASSWORD

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
