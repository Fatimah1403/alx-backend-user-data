#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user and
            return User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        method takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered
        by the method’s input arguments.
        """
        if not kwargs:
            raise InvalidRequestError
        user_data = self._session.query(User).filter_by(**kwargs).first()
        if not user_data:
            raise NoResultFound
        return user_data

    def update_user(self, user_id: int, **kwargs) -> None:
        """_summary_

        Args:
            user_id (_type_): method will use find_user_by
            to locate the user to update
        """
        user_rec = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if hasattr(user_rec, key):
                setattr(user_rec, key, value)
            else:
                raise ValueError

        self._session.commit()
        return None
