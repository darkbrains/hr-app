import os
import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        reset = "\033[00m"
        FORMATS = {
            "DEBUG": "\033[37m",
            "INFO": "\033[38m",
            "WARNING": "\033[33m",
            "ERROR": "\033[31m",
            "CRITICAL": "\033[35m",
        }
        log_message = {
            "module": record.module,
            "filename": record.filename,
            "lineno": record.lineno,
            "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_message["exception"] = self.formatException(record.exc_info)
        message = json.dumps(log_message)
        if os.environ.get("COLORED_LOGS"):
            message = FORMATS[record.levelname] + message + reset
        return message

def _setup_logger():
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger()
    logger.handlers = []  # Remove all handlers associated with the root logger.
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger

logger = _setup_logger()
