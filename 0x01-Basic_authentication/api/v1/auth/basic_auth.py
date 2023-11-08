#!/usr/bin/env python3
"""Class BasicAuth"""
from api.v1.auth.auth import Auth
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """ Basic Authentication inheriting from Auth """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of a Base64
        string base64_authorization_header: """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password
        from the Base64 decoded value."""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
             that returns the User instance based on his email and password.
            Return None if user_email is None or not a string
            Return None if user_pwd is None or not a string
            Return None if your database (file) doesn’t contain any
            User instance with email equal to user_email - you should
            use the class method search of the User to lookup the list
            of users based on their email. Don’t forget to test
            all cases: “what if there is no user in DB?”, etc.
            Return None if user_pwd is not the password of
            the User instance found - you must use
            the method is_valid_password of User
            Otherwise, return the User instance
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        try:
            auth_header = self.authorization_header(request)
            # Decode auth header value, get user data using Basic Auth methods
            encode_header = self.extract_base64_authorization_header(
                    auth_header)
            decoded_header = self.decode_base64_authorization_header(
                    encode_header)
            user_creds = self.extract_user_credentials(decoded_header)
            return self.user_object_from_credentials(*user_creds)
        except Exception:
            return None
