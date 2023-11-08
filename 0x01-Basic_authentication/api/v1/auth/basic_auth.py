#!/usr/bin/env python3
"""module for Basic Auth"""


from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
from models.base import Base


class BasicAuth(Auth):
    """class for Basic authorisation that is based on base authorisation class
    """

    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """ method that returns Base64 part of the Authorization header
          in basic authentication
        """
        if authorization_header is None:
            return None
        if str(authorization_header).startswith("Basic ") is False:
            return None
        # if authorization_header.__str__ is None:
        #     return None
        # return str(authorization_header)[len("Basic "):]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """ method that decodes the authorization header and gives the username
        and password string originally input
        """
        if base64_authorization_header is None:
            return None
        if isinstance(base64_authorization_header, str) is False:
            return None

        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            base64_bytes_decoded = base64.b64decode(base64_bytes)

            return base64_bytes_decoded.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ method to extract user credentials i.e. user email and password
        from a Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if isinstance(decoded_base64_authorization_header, str) is False:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        result = decoded_base64_authorization_header.split(":")
        key = result[0]
        value = result[1]
        return key, value

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """ method that returns the user based on his/her
        email and password
        """
        # user = User()
        # db_path = user.load_from_file()

        if user_email is None or user_pwd is None:
            return None

        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        User()

        users = User.search({'email': user_email})
        # print(users_list)

        if not users or users == []:
            return None

        try:
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None
