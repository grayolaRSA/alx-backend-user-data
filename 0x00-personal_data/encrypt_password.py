#!/usr/bin/env python3
"""module to hash passwords"""


import bcrypt
from bcrypt import hashpw, checkpw


def hash_password(password: str) -> bytes:
    """function that hashes passwords"""
    return hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if password is valid"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
