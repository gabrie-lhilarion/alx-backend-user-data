#!/usr/bin/env python3
"""
DB module

This module defines the DB class, which handles the database operations
for the User model. It includes methods to initialize the database and
add new users to the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class

    This class provides an interface to interact with the database,
    including initializing the database and adding new users.
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
        """
        Adds a new user to the database.

        Args:
            email (str): The email address of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created `User` object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session  # Get the session from the private property
        session.add(new_user)
        session.commit()
        return new_user
