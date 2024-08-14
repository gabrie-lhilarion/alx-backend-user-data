#!/usr/bin/env python3
"""
This module defines the Auth class for handling user
registration and authentication.
"""

from db import DB
from db import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the given email and password.

        Args:
            email (str): The email of the user to register.
            password (str): The password of the user to register.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Check if a user with the given email already exists
            self._db.find_user_by(email=email)
            # If the user is found, raise a ValueError
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If no user is found, proceed to create a new user
            hashed_password = self._db._hash_password(password)
            user = self._db.add_user(
                email=email, hashed_password=hashed_password.decode('utf-8')
            )
            return user
