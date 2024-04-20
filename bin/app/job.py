import asyncio
from utils.email_resend import resend_emails
from utils.logger import logger

try:
    asyncio.run(resend_emails())
    logger.info('The resend_emails function completed successfully.')
except Exception as e:
    logger.error(f'Unexpected error occurred: {e}')
