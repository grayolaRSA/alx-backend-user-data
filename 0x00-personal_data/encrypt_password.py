#!/usr/bin/env python3
"""module to hash passwords"""


import bcrypt
from bcrypt import hashpw, checkpw


def hash_password(password: str) -> bytes:
    """function that hashes passwords"""

    return hashpw(b"password", bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if password is valid"""
    return checkpw(b"password", hashed_password)
