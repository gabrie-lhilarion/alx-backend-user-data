#!/usr/bin/env python3
"""
Auth module for API authentication management
"""
from flask import request
from typing import List, TypeVar
# from models.user import User

User = TypeVar('User')


class Auth:
    """Class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to determine if authentication is required.
        Currently returns False as a placeholder.
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        # Ensure path always ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        for ex_path in excluded_paths:
            if ex_path.endswith('/') and ex_path == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to get the authorization header from the request.
        Currently returns None as a placeholder.
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Method to get the current user from the request.
        Currently returns None as a placeholder.
        """
        return None
