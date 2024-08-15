#!/usr/bin/env python3
"""
Test module for user authentication routes.

Each function tests a specific route or scenario.
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a user with the provided email and password.
    Asserts that the response has the correct status code and payload.
    """
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the wrong password.
    Asserts that the response has the correct status code.
    """
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Log in with the correct credentials.
    Asserts that the response has the correct status code and payload.
    Returns the session ID.
    """
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 200
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    assert response.json() == {"email": email, "message": "logged in"}
    return session_id


def profile_unlogged() -> None:
    """
    Attempt to access the profile without being logged in.
    Asserts that the response has the correct status code.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Access the profile while logged in.
    Asserts that the response has the correct status code and payload.
    """
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    Log out from the session.
    Asserts that the response has the correct status code.
    """
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Request a reset password token.
    Asserts that the response has the correct status code and payload.
    Returns the reset token.
    """
    response = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email}
    )
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert reset_token is not None
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the password using the reset token.
    Asserts that the response has the correct status code and payload.
    """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(f"{BASE_URL}/reset_password", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


# Constants for the test
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

# Main execution
if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
