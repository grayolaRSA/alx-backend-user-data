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
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        expected_path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            normalized_excluded = excluded_path if excluded_path.endswith('/')\
                 else excluded_path if excluded_path.endswith('*')

            if expected_path.startswith(normalized_excluded):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """method that returns None when flask request made
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None when flask request made
        """
        if request is None:
            return None
        return None
