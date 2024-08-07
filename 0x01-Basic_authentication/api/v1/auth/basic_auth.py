#!/usr/bin/env python3
"""
BasicAuth module for API authentication
management
"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, Optional
from typing import Tuple, Optional, TypeVar
from models.user import User

UserType = TypeVar('User')


class BasicAuth(Auth):
    """Class to manage basic authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization
            header from the request.

        Returns:
            str: The Base64 part of the Authorization
            header or None if invalid.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """
        Decodes the Base64 part of the Authorization header.

        Args:
            base64_authorization_header (str): The Base64
            encoded part of the Authorization header.

        Returns:
            str: The decoded value as a UTF-8 string or
            None if invalid.
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(
                base64_authorization_header
            )
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts the user email and password from the
        Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str):
            The decoded Base64 string.

        Returns:
            tuple: The user email and password,
            or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> Optional[UserType]:
        """
        Returns the User instance based on email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance or None if invalid.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        user = User.search(user_email)
        if user is None or not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> Optional[UserType]:
        """
        Retrieves the User instance for a request.

        Args:
            request: The Flask request object.

        Returns:
            User: The User instance or None if invalid.
        """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None

        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
