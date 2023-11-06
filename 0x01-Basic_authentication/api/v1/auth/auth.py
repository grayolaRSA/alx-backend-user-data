#!/usr/bin/env python3
"""Basic authorization module"""


from flask import request
from typing import List, TypeVar


class Auth:
    """Basic Authorization class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """method that returns False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """method that returns None when flask request made
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None when flask request made
        """
        return None
