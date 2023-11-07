#!/usr/bin/env python3
"""module for Basic Auth"""


from api.v1.auth.auth import Auth
import base64


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
        if authorization_header.__str__ is None:
            return None
        return str(authorization_header)[len("Basic "):]

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
