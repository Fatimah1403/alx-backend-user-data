#!/usr/bin/env python3
"""
function called filter_datum
"""
import logging
import re
import mysql.connector
from typing import List


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
