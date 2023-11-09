#!/usr/bin/env python3
"""Session authorization module"""


from flask import request
from .auth import Auth
import uuid


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
        session_id = uuid.uuid4()
        user_id_by_session_id = {session_id: user_id}
        return user_id_by_session_id
