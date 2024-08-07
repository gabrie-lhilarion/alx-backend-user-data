#!/usr/bin/env python3
"""
BasicAuth module for API authentication management
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Class to manage basic authentication"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Authentication.
        
        Args:
            authorization_header (str): The Authorization header from the request.

        Returns:
            str: The Base64 part of the Authorization header or None if invalid.
        """
        if authorization_header is None:
            return None
        
        if not isinstance(authorization_header, str):
            return None
        
        if not authorization_header.startswith("Basic "):
            return None
        
        return authorization_header[len("Basic "):]
