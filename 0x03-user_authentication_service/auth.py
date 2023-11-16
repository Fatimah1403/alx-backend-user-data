#!/usr/bin/env python3
"""Authentication
"""
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4
from user import User
from db import DB
from typing import Union


def _hash_password(password: str) -> bytes:
    """_summary_

    Args:
        password (str): _description_

    Returns:
        bytes: _description_
    """
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """
    Generates UUID
    Returns string representation of new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """_summary_

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            User: _description_
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """
        It should expect email and password required arguments and return a boolean.  # noqa: E501

        Try locating the user by email. If it exists, check the password with bcrypt.checkpw.  #  noqa: E501
        If it matches return True. In any other case, return False.
        """
        try:
            user_login = self._db.find_user_by(email=email)
            return checkpw(password.encode("utf-8"), user_login.hashed_password)  # noqa: E501
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        create_session method. It takes an email string argument
        and returns the session ID as a string.
        The method should find the user corresponding to the email,
        generate a new UUID and store it in the database as
        the user’s session_id, then return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Finds user by session_id """
        if session_id is None:
            return None
        try:
            found_user = self._db.find_user_by(session_id=session_id)
            return found_user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user’s session ID to None"""
        if user_id is None:
            return None
        try:
            found_user = self._db.find_user_by(id=user_id)
            self._db.update_user(found_user.id, session_id=None)

        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Find the user corresponding to the email.
        If the user does not exist, raise a ValueError exception.
        If it exists, generate a UUID and update the user’s
        reset_token database field. Return the token.
        """
        if email is None or not isinstance(email, str):
            raise ValueError
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError


def update_password(self, reset_token: str, password: str) -> None:
    """update the user’s hashed_password

    Args:
        reset_token (str): _description_
        password (str): _description_

    Returns:
        _type_: _description_
    """
    if reset_token is None or not isinstance(reset_token, str):
        raise ValueError from None
    if password is None or not isinstance(password, str):
        raise ValueError from None
    try:
        user = self._db.find_user_by(reset_token=reset_token)
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, reset_token=None,
                             hashed_password=hashed_password)
        return None
    except NoResultFound:
        raise ValueError from None
