import asyncio
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.logger import logger
from utils.envs import EMAIL_ADDRESS, EMAIL_PASSWORD
from utils.db_operations import create_db_connection


email_verification_texts = {
    'en': "Your verification code is: {}. This code will expire in 5 minutes.",
    'ru': "Ваш проверочный код: {}. Код будет действителен в течение 5 минут.",
    'hy': "Ձեր հաստատման կոդը՝ {}. Այս կոդը կանցնի 5 րոպեից։"
}


email_contents = {
    'en': {
        'rejection_subject': "Thank You for Your Participation",
        'rejection_message': (
            "Thank you for your time and patience throughout the interview process.\n\n"
            "We regret to inform you that your result did not qualify for the next stage of the recruitment process.\n\n"
            "We wish you all the best in your future endeavors.\n\n"
            "Best regards,\nThe People Connect Team"
        ),
        'invitation_subject': "Congratulations - Next Steps in People Connect",
        'invitation_message': (
            "Congratulations on successfully passing the initial screening!\n\n"
            "We are pleased to invite you to the next interview stage for a specific position with our company.\n\n"
            "We will notify you of further actions within 2 business days.\n\n"
            "Best regards,\nThe People Connect Team"
        )
    },
    'ru': {
        'rejection_subject': "Спасибо за ваше участие",
        'rejection_message': (
            "Благодарим вас за время и терпение в течение всего процесса собеседования.\n\n"
            "К сожалению, мы должны сообщить, что вы не прошли в следующий этап процесса подбора персонала.\n\n"
            "Желаем вам успехов в будущих начинаниях.\n\n"
            "С уважением,\nКоманда People Connect"
        ),
        'invitation_subject': "Поздравляем - Следующие шаги в People Connect",
        'invitation_message': (
            "Поздравляем с успешным прохождением начального отбора!\n\n"
            "Мы рады пригласить вас на следующий этап собеседования на конкретную должность в нашей компании.\n\n"
            "Мы уведомим вас о дальнейших действиях в течение 2 рабочих дней.\n\n"
            "С уважением,\nКоманда People Connect"
        )
    },
    'hy': {
        'rejection_subject': "Շնորհակալություն մասնակցության համար",
        'rejection_message': (
            "Շնորհակալություն ձեր ժամանակի և համարձակության համար ընդհանուր հանդիպման ընթացքում։\n\n"
            "Ցավոք, պետք է հայտնել, որ ձեր արդյունքը չի հաջողվել հաջորդ փուլին։\n\n"
            "Մենք ձեզ մեծ հաջողություն մաղթում ենք ձեր ապագա ձեռնարկություններում։\n\n"
            "Բարեհաջողներով,\nPeople Connect թիմը"
        ),
        'invitation_subject': "Շնորհավորումներ - Հաջորդ քայլերը People Connect-ում",
        'invitation_message': (
            "Շնորհավորումներ հաջողակ անցումով նախնական ընտրություններից։\n\n"
            "Մենք ուրախ ենք հրավիրել ձեզ մեր կոմպանիայի որոշակի դիրքի հաջորդ փուլի հանդիպմանը։\n\n"
            "Մենք կծանուցենք ձեզ հաջորդ ակտիվությունների մասին 2 աշխատանքային օրերի ընթացքում։\n\n"
            "Բարեհաջողներով,\nPeople Connect թիմը"
        )
    }
}


def send_email(receiver_email, code, lang='en'):
    try:
        text = email_verification_texts.get(lang, email_verification_texts).format(code)
        message = MIMEMultipart("alternative")
        message["Subject"] = "Verification Code"
        message["From"] = EMAIL_ADDRESS
        message["To"] = receiver_email
        part1 = MIMEText(text, "plain")
        message.attach(part1)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, receiver_email, message.as_string())
            logger.info(f"Verification email sent to {receiver_email} in {lang}")

    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred while sending email to {receiver_email}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred while sending email to {receiver_email}: {e}")


def update_email_status(email, status):
    conn = create_db_connection()
    if conn is None:
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


def send_custom_email(receiver_email, subject, message, lang='en'):
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
            logger.info(f"Custom email sent to {receiver_email} with subject: '{subject}' in {lang}")

    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred while sending email to {receiver_email}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred while sending email to {receiver_email}: {e}")


async def send_email_with_delay(email, score, lang):
    try:
        if score < 50:
            await send_rejection_email(email, lang)
        else:
            await send_invitation_email(email, lang)
    except Exception as e:
        logger.error(f'Error in send_email_with_delay() function: {e}')


async def send_rejection_email(receiver_email, lang='en'):
    content = email_contents.get(lang)
    try:
        subject = content['rejection_subject']
        message = content['rejection_message']
        await asyncio.sleep(900)
        send_custom_email(receiver_email, subject, message)
        logger.info(f"Rejection email sent to {receiver_email} in {lang}")
        update_email_status(receiver_email, True)
    except Exception as e:
        logger.error(f'Error in send_rejection_email() function: {e}')

async def send_invitation_email(receiver_email, lang='en'):
    content = email_contents.get(lang)
    try:
        subject = content['invitation_subject']
        message = content['invitation_message']
        await asyncio.sleep(900)
        send_custom_email(receiver_email, subject, message)
        logger.info(f"Invitation email sent to {receiver_email} in {lang}")
        update_email_status(receiver_email, True)
    except Exception as e:
        logger.error(f'Error in send_invitation_email() function: {e}')
