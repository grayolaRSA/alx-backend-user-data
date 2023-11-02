#!/usr/bin/env python3
"""module that obfuscates the log message"""


import re


def filter_datum(fields: list, redaction: str, message: str,
                 separator: str) -> str:
    """function to filter data"""
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+',
                  f'\\1={redaction}', message)
