#!/usr/bin/env python3

"""
This module provides a function to obfuscate specified fields in a log message
and a custom logging formatter to apply this obfuscation to log records.

The function uses regular expressions to identify and replace the values of the
specified fields with a redaction string.
"""

import logging
import os
import re
import mysql.connector
from mysql.connector.connection import MySQLConnection
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
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
            fields (List[str]): A list of strings representing all fields to
            obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted and obfuscated log record.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Create and configure a logger named 'user_data'.

    The logger will log messages up to logging.INFO
    level and will not propagate messages to other
    loggers. It will have a StreamHandler with a
    RedactingFormatter as its formatter.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    logger.addHandler(handler)

    return logger

def get_db() -> MySQLConnection:
    """
    Obtain a connection to the secure Holberton database.

    Uses environment variables to retrieve database credentials.

    Returns:
        MySQLConnection: A connector to the database.
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

def main() -> None:
    """
    Main function to retrieve and log data
    from the users table.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")

    logger = get_logger()
    
    for row in cursor:
        message = "; ".join(f"{k}={v}" for k, v in row.items())
        logger.info(message)

    cursor.close()
    db.close()