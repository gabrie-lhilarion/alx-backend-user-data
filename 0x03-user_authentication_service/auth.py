#!/usr/bin/env python3
"""
This module defines the Auth class for handling user
registration and authentication.
"""

import uuid
import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def get_user_from_session_id(
            self, session_id: Optional[str]
    ) -> Optional[User]:
        """
        Retrieve a User from the database using a session ID.

        Args:
            session_id (str): The session ID used to find the user.

        Returns:
            User: The User object if found, or None if no user is found or if
            session_id is None.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

        return user

    def _generate_uuid(self) -> str:
        """
        Generate a new UUID.

        This method is private and should not be used outside the auth module.

        Returns:
            str: The string representation of a new UUID.
        """
        return str(uuid.uuid4())

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a password reset token for a user identified by
        the provided email.

        Args:
            email (str): The email of the user requesting the reset token.

        Returns:
            str: The generated reset token.

        Raises:
            ValueError: If no user is found with the provided email.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # Raise a ValueError if the user does not exist
            raise ValueError(f"No user found with email: {email}")

        # Generate a new UUID for the reset token
        reset_token = self._generate_uuid()

        # Update the user's reset_token in the database
        self._db.update_user(user.id, reset_token=reset_token)

        # Return the generated reset token
        return reset_token

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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate the user's login credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password.encode('utf-8')
            )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user identified by the provided email.

        Args:
            email (str): The user's email address.

        Returns:
            str: The session ID (UUID) for the new session.

        Raises:
            NoResultFound: If no user with the provided email is found.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)

            # Generate a new UUID for the session ID
            session_id = self._generate_uuid()

            # Update the user's session_id with the new UUID
            self._db.update_user(user.id, session_id=session_id)

            # Return the session ID
            return session_id
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session by setting their session ID to None.

        Args:
            user_id (int): The ID of the user whose session is to be destroyed.

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except Exception:
            pass

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the user's password.

        Args:
            reset_token (str): The reset token associated with the user.
            password (str): The new password to be hashed and saved.

        Raises:
            ValueError: If the reset_token does not match any user.
        """
        try:
            # Find the user by reset_token
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            # Raise an error if no user is found with the reset_token
            raise ValueError("Invalid reset token")

        # Hash the new password
        hashed_password = self._hash_password(password)

        # Update the user's password and reset_token
        self._db.update_user(
            user.id, hashed_password=hashed_password, reset_token=None
        )
