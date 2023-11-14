#!/usr/bin/env python3
"""authentication module"""


import bcrypt
from bcrypt import hashpw
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound, InvalidRequestError


def _hash_password(password: str) -> bytes:
    """function that hashes passwords"""
    return hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        method to register user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")

        except NoResultFound:
            hashed_pw = _hash_password(password)

            new_user = self._db.add_user(email, hashed_pw)

            self._db._session.add(new_user)
            self._db._session.commit()
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        method to validate a user login
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode('utf-8'),
                                      user.hashed_password)
        except NoResultFound:
            return False
