#!/usr/bin/env python3
"""
function called filter_datum
"""
import logging
import re
from mysql.connector import connection
from typing import List
import os


#  fields to be obfuscated
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    The function should use a regex to replace
    occurrences of certain field values.
    filter_datum should be less than 5 lines long and use
    """
    log_line = message
    for field in fields:
        log_line = re.sub(field + "=.*?" + separator,
                          field + "=" + redaction + separator, log_line)
    return log_line


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ inits class instance """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filters values in incoming log records """
        return filter_datum(
            self.fields, self.REDACTION, super(
                RedactingFormatter, self).format(record),
            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object.
            It should have a StreamHandler with
            RedactingFormatter as formatter.
    """
    logger = logging.getLogger(name="user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    str_handler = logging.StreamHandler()
    str_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(str_handler)
    return logger
