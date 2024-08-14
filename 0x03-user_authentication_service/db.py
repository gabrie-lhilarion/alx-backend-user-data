#!/usr/bin/env python3
"""
DB module

This module defines the DB class, which handles the database operations
for the User model. It includes methods to initialize the database and
add new users to the database.
"""

import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
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

    def _hash_password(self, password: str) -> bytes:
        """
        Hashes a password string using bcrypt and returns the salted hash.

        Args:
            password (str): The password string to hash.

        Returns:
            bytes: The salted hash of the input password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    
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

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments representing the field(s)
                      and value(s) to filter the users.

        Returns:
            User: The first User object that matches the criteria.

        Raises:
            NoResultFound: If no user is found with the specified criteria.
            InvalidRequestError: If invalid query arguments are provided.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the provided criteria.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments provided.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing the field(s)
                      and value(s) to update the user with.

        Returns:
            None

        Raises:
            ValueError: If an argument that does not correspond to a user
                        attribute is passed.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"{key} is not a valid attribute of User")
            setattr(user, key, value)
        self._session.commit()
