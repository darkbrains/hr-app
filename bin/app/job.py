import asyncio
from utils.email_resend import resend_emails
from utils.logger import logger

async def main():
    try:
        await resend_emails()
        logger.info('The resend_emails function completed successfully.')
    except Exception as e:
        logger.error(f'Unexpected error occurred: {e}')

if __name__ == "__main__":
    asyncio.run(main())
