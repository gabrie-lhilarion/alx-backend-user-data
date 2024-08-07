#!/usr/bin/env python3
"""
Auth module for API authentication management
"""
from flask import request
from typing import List, TypeVar
from fnmatch import fnmatch

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

        if excluded_paths is None or not excluded_paths:
            return True

        path = path.rstrip('/')
        for excluded_path in excluded_paths:
            if fnmatch(path, excluded_path.rstrip('/')):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to get the authorization header from the request.
        Currently returns None as a placeholder.
        """
        if request is None:
            return None

        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request=None) -> User:
        """
        Method to get the current user from the request.
        Currently returns None as a placeholder.
        """
        return None
