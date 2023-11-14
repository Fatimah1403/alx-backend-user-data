#!/usr/bin/env python3
""" class user """
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """Users table
    """
    __tablename__ = "users"
    # __table_args__ = {"mysql_default_charset": "latin1"}
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
