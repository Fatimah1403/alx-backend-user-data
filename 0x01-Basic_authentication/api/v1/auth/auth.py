#!/usr/bin/env python3
"""
API Authentication
"""

from flask import request
from os import getenv
from typing import List, TypeVar


class Auth:
    """Auth class to manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """To determine whether authentication
            is required for an API route
        """
        if path is None or not excluded_paths:
            return True
        for i in excluded_paths:
            if i.endswith('*') and path.startwith(i[:-1]):
                return False
            elif i in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        To check whether Authorization request header is present
        """
        if request is None or "Authorization" not in request.headers:
            return None
        else:
            req_header = request.headers.get('Authorization')
            return req_header

    def def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request """
        return None
