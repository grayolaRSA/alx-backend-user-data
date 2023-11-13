#!/usr/bin/env python3
"""authentication module"""


import bcrypt
from bcrypt import hashpw


def _hash_password(password: str) -> bytes:
    """function that hashes passwords"""
    return hashpw(password.encode('utf-8'), bcrypt.gensalt())
