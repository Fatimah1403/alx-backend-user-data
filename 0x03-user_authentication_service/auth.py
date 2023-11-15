#!/usr/bin/env python3
"""Authentication
"""
from bcrypt import hashpw, gensalt
from user import User
from db import DB


def _hash_password(password: str) -> bytes:
    """_summary_

    Args:
        password (str): _description_

    Returns:
        bytes: _description_
    """
    return hashpw(password.encode("utf-8"), gensalt())
