#!/usr/bin/env python3
"""module to hash passwords"""


import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """function that hashes passwords"""
    return hashpw(b"password", bcrypt.gensalt())
