#!/usr/bin/env python3
"""
Hashing with bcrypt
"""
import bcrypt
from bcrypt import hashpw

def hash_password(password):
    """returns a salted, hashed password"""
    password = password.encode()
    hash_pass = hashpw(passsword, bcrypt.gensalt())
    return hash_pass
