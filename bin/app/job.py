import asyncio
from utils.email_resend import resend_emails, update_message_status
from utils.phone_message_resend import resend_messages
from utils.logger import logger


async def main():
    try:
        await resend_messages()
        logger.info('The resend_messages function completed successfully.')
        await resend_emails()
        logger.info('The resend_emails function completed successfully.')
    except Exception as e:
        logger.error(f'Unexpected error occurred: {e}')

if __name__ == "__main__":
    asyncio.run(main())
