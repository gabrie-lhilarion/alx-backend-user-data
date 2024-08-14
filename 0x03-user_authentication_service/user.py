#!/usr/bin/env python3
"""
This module defines the SQLAlchemy model for the `users` table.

The `User` model includes attributes such as `id`, `email`, `hashed_password`,
`session_id`, and `reset_token`. These fields represent the primary key,
email address, hashed password, session ID, and password reset token,
respectively.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): The primary key of the user.
        email (str): The email address of the user. Non-nullable.
        hashed_password (str): The hashed password of the user. Non-nullable.
        session_id (str): The session identifier of the user. Nullable.
        reset_token (str): The reset token for password recovery. Nullable.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
