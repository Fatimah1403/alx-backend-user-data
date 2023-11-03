#!/usr/bin/env python3
"""
Hashing with bcrypt
"""
import bcrypt
from bcrypt import hashpw

def hash_password(password):
    """returns a salted, hashed password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
