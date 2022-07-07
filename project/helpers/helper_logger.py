import logging
import os

from logtail import LogtailHandler

"""
CRITICAL = 50
ERROR = 40
WARN = 30
INFO = 20
"""


class Logger:
    @staticmethod
    def create_logger():
        handler = LogtailHandler(source_token=os.environ.get("LOG_SOURCE_TOKEN"))
        logger = logging.getLogger(__name__)
        logger.handlers = []
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def info(message):
        logger = Logger.create_logger()
        logger.info(message)

    @staticmethod
    def warn(message):
        logger = Logger.create_logger()
        logger.warn(message)

    @staticmethod
    def error(message):
        logger = Logger.create_logger()
        logger.error(message)

    @staticmethod
    def critical(message):
        logger = Logger.create_logger()
        logger.critical(message)
