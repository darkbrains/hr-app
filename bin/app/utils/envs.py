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

logger.debug(f"Configured database host: {DATABASE_HOST}")
logger.debug(f"Configured database user: {DATABASE_USER}")
logger.debug(f"Configured database name: {DATABASE_NAME}")
logger.debug(f"Configured database port: {DATABASE_PORT}")
logger.debug(f"Configured email address: {EMAIL_ADDRESS}")
logger.debug(f"Configured salt passoword: {SALT_PASSWORD}")