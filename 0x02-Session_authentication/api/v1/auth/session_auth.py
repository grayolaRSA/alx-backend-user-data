#!/usr/bin/env python3
"""Basic authorization module"""


from flask import request
from .auth import Auth


class SessionAuth(Auth):
    """Basic Authorization class
    """
    pass
