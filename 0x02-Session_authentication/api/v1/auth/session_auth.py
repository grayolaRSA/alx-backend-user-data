#!/usr/bin/env python3
"""Session authorization module"""


from flask import request
from .auth import Auth
import uuid
from typing import Dict
from models.user import User


class SessionAuth(Auth):
    """Session Authorization class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        method that creates a session ID for a user ID
        """

        if not isinstance(user_id, str) or user_id is None:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        method to get a user ID related to a session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        # user_id_by_session_id = {}
        # for session_id, v in user_id_by_session_id:
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        returns user instance based on a cookie value
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_by_session_id(session_cookie)
        user = User.get(user_id)
        return user
