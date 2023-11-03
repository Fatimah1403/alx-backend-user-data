#!/uisr/bin/env python3
"""
Hashing with bcrypt
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password"""
    b = password.encode()
    hashed = hashpw(b, bcrypt.gensalt("utf-8"))
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password matches the hashed password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
