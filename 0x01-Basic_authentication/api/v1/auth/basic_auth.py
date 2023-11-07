#!/usr/bin/env python3
"""module for Basic Auth"""


from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """class for Basic authorisation that is based on base authorisation class
    """
    
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ method that returns Base64 part of the Authorization header in basic authentication
        """
        if authorization_header is None:
            return None 
        if str(authorization_header).startswith("Basic ") is False:
            return None
        if authorization_header.__str__ is None:
            return None
        return str(authorization_header)[len("Basic "):]
