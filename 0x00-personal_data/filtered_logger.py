#!/usr/bin/env python3
"""module that obfuscates the log message"""


import re
import logging


def filter_datum(fields: list, redaction, message, separator: str) -> str:
    """function to filter data"""
    pattern = r'(' + '|'.join(fields) + r')=[^' + separator + ']+'
    return re.sub(pattern, r'\1=' + redaction, message)
    # return re.sub(fr'({"|".join(fields)})=[^{separator}]+', f'\\1={redaction}',
                #   message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields_to_redact = fields if fields else []

    def format(self, record: logging.LogRecord) -> str:
        """format method to filter data according to classes"""
        log_message = super(RedactingFormatter, self).format(record)
        log_message_output = filter_datum(self.fields_to_redact,
                                          self.REDACTION,
                                          log_message, self.SEPARATOR)
        return log_message_output
