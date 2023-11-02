#!/usr/bin/env python3
"""module that obfuscates the log message"""


import re
import logging
from logging import StreamHandler
from typing import Tuple, List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """function to filter data"""
    pattern = r'(' + '|'.join(fields) + r')=[^' + separator + ']+'
    return re.sub(pattern, r'\1=' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields_to_redact = fields if fields else []

    def format(self, record: logging.LogRecord) -> str:
        """format method to filter data according to classes"""
        log_message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields_to_redact, self.REDACTION,
                            log_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """function to return logger object"""

    logger = logging.getLogger("user_data")

    logger.setLevel(logging.INFO)

    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
