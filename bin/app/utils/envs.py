import os
from utils.logger import logger

def get_env_variable(var_name, default=None):
    try:
        return os.environ[var_name]
    except KeyError:
        if default is None:
            logger.error(f"Environment variable {var_name} not set and no default provided.")
            raise
        logger.warning(f"Environment variable {var_name} not set; using default value.")
        return default

TOTAL_QUESTIONS = 20
DATABASE_HOST = get_env_variable('MYSQL_HOST')
DATABASE_USER = get_env_variable('MYSQL_USER')
DATABASE_PASSWORD = get_env_variable('MYSQL_PASSWORD')
DATABASE_NAME = get_env_variable('MYSQL_DB')
DATABASE_PORT = get_env_variable('MYSQL_PORT', '3306')
EMAIL_ADDRESS = get_env_variable('EMAIL_ADDRESS')
EMAIL_PASSWORD = get_env_variable('EMAIL_PASSWORD')
SALT_PASSWORD = get_env_variable('SALT_PASSWORD', 'yl98!W9FHN')
PORT = get_env_variable('PORT', '8085')
ZADARMA_API_KEY = get_env_variable('ZADARMA_API_KEY')
ZADARMA_API_SECRET = get_env_variable('ZADARMA_API_SECRET')

logger.info(f"Configured database host: {DATABASE_HOST}")
logger.info(f"Configured database user: {DATABASE_USER}")
logger.info(f"Configured database name: {DATABASE_NAME}")
logger.info(f"Configured database port: {DATABASE_PORT}")
logger.info(f"Configured email address: {EMAIL_ADDRESS}")
logger.info(f"Configured salt passoword: {SALT_PASSWORD}")
logger.info(f"Configured port: {PORT}")
logger.info(f"Configured zadarma api_key: {ZADARMA_API_KEY}")
logger.info(f"Configured zadarma api_secret: {ZADARMA_API_SECRET}")
