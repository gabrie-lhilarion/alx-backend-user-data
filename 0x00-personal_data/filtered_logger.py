#!/usr/bin/env python3

"""
This module provides a function to obfuscate specified fields in a log message
and a custom logging formatter to apply this obfuscation to log records.

The function uses regular expressions to identify and replace the values of the
specified fields with a redaction string.
"""

import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obfuscates specified fields in a log message."""
    pattern = f'({"|".join(fields)})=([^ {separator}]+)'
    return re.sub(pattern, lambda m: f'{m.group(1)}={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with specified fields to obfuscate.

        Args:
            fields (List[str]): A list of strings representing all fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record, obfuscating specified fields."""
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
