#!/usr/bin/env python3
"""Class BasicAuth"""
from api.v1.auth.auth import Auth
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """ Basic Authentication inheriting from Auth """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]