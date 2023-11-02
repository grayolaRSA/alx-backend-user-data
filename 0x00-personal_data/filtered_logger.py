#!/usr/bin/env python3
"""module that obfuscates the log message"""


import re
import logging
from logging import StreamHandler
from typing import Tuple, List
import os
import mysql.connector


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """a function to establish a mysql connection to a database"""
    db_host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_user = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return connection  # Return the MySQLConnection object
    except mysql.connector.Error as err:
        # Handle connection errors
        print(f"Error: {err}")
        return None  # Return None to indicate an error
