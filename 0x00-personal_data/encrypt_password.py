#!/uisr/bin/env python3
"""
Hashing with bcrypt
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Hash a password using Bcrypt """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validate hashed password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
