#!/usr/bin/env python3
"""
Hashes a password string using bcrypt and returns the salted hash.
"""

import bcrypt


def _hash_password(password: str) -> bytes:
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
