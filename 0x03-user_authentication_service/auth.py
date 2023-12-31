#!/usr/bin/env python3
"""authentication module"""


import bcrypt
from bcrypt import hashpw
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound, InvalidRequestError
import uuid
from typing import Union


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

    def _generate_uuid(self) -> str:
        """"
        generates new uuid to be used in Auth
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        generates a session ID based on a valid email login
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = self._generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        method that gets the user that corresponds with a session id
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except ValueError:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        method to destroy the session by removing the session id
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except NoResultFound:
            return ValueError('no related user ID found')

    def get_reset_password_token(self, email: str) -> str:
        """
        method to generate reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)

        except NoResultFound:
            raise ValueError

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        method that updates password after user requests reset token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)

            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)

        except NoResultFound:
            raise ValueError
