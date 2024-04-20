import asyncio
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.logger import logger
from utils.envs import EMAIL_ADDRESS, EMAIL_PASSWORD
from utils.db_operations import create_db_connection

email_verification_texts = {
    'en': {
        'message': "Your verification code is",
        'header': "Verification Needed",
        'footer': "Best regards,<br>People Connect Team"
    },
    'ru': {
        'message': "Ваш проверочный код",
        'header': "Требуется верификация",
        'footer': "С уважением,<br>People Connect Team"
    },
    'hy': {
        'message': "Ձեր հաստատման կոդը",
        'header': "Պահանջվում է վերահսկում",
        'footer': "Հարգանքներով,<br>People Connect Team"
    }
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

html_template = """
<html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333333;
                margin: 0;
                padding: 0;
            }}
            .container {{
                background-color: #ffffff;
                width: 100%;
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                text-align: center;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,.05);
            }}
            .header {{
                background-color: #b1dbdb;
                color: #ffffff;
                padding: 10px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            .code {{
                font-size: 24px;
                margin: 20px;
                padding: 10px 0;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 14px;
                color: #777777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{header}</h1>
            </div>
            <p>{body}</p>
            <div class="code">
                {code}
            </div>
            <p class="footer">
                {footer}
            </p>
        </div>
    </body>
</html>
"""

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


def send_email(receiver_email, code, lang='en'):
    try:
        content = email_verification_texts[lang]
        text = content['message'].format(code)
        html_message = html_template.format(
            header=content['header'],
            body=text,
            code=code,
            footer=content['footer']
        )
        message = MIMEMultipart("alternative")
        message["Subject"] = content['header']
        message["From"] = "People Connect Team"
        message["To"] = receiver_email
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html_message, "html")
        message.attach(part1)
        message.attach(part2)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, receiver_email, message.as_string())
            logger.info(f"Verification email sent to {receiver_email} in {lang}")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred while sending email to {receiver_email}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred while sending email to {receiver_email}: {e}")


def send_custom_email(receiver_email, subject, content, lang):
    html_message = html_template.format(
        header=content['header'],
        body=content['message'],
        code=content.get('code', ''),
        footer='Best regards,<br>The People Connect Team'
    )
    mime_message = MIMEMultipart("alternative")
    mime_message["Subject"] = subject
    mime_message["From"] = "People Connect Team"
    mime_message["To"] = receiver_email
    mime_message.attach(MIMEText(html_message, "html"))
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(mime_message)
            logger.info(f"Email sent to {receiver_email} in {lang}")
    except Exception as e:
        logger.error(f"Error sending email to {receiver_email}: {e}")


async def send_email_with_delay(email, score, lang='en'):
    try:
        if score < 50:
            await send_rejection_email(email, lang)
        else:
            await send_invitation_email(email, lang)
    except Exception as e:
        logger.error(f'Error processing email sending with delay for {email}: {e}')


async def send_rejection_email(receiver_email, lang='en'):
    try:
        content = email_contents.get(lang, {})
        rejection_content = {
            'header': content['rejection_subject'],
            'message': content['rejection_message']
        }
        await asyncio.sleep(900)
        await send_custom_email(receiver_email, content['rejection_subject'], rejection_content, lang)
        update_email_status(receiver_email, True)
        logger.info(f"Rejection email sent to {receiver_email}")
    except Exception as e:
        logger.error(f'Error sending rejection email to {receiver_email}: {e}')


async def send_invitation_email(receiver_email, lang='en'):
    try:
        content = email_contents.get(lang, {})
        invitation_content = {
            'header': content['invitation_subject'],
            'message': content['invitation_message']
        }
        await asyncio.sleep(900)
        await send_custom_email(receiver_email, content['invitation_subject'], invitation_content, lang)
        update_email_status(receiver_email, True)
        logger.info(f"Invitation email sent to {receiver_email}")
    except Exception as e:
        logger.error(f'Error sending invitation email to {receiver_email}: {e}')
