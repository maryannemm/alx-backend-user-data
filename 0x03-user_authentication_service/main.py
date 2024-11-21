#!/usr/bin/env python3
"""
End-to-End (E2E) Integration Test for `app.py`.

This script tests the functionality of a user authentication system. 
It covers user registration, login/logout, profile access, and password reset workflows.
"""

from typing import Optional
import requests

# Configuration
BASE_URL = "http://0.0.0.0:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """
    Test user registration.

    Ensures that a user can register successfully and handles duplicate email attempts.
    """
    url = f"{BASE_URL}/users"
    payload = {'email': email, 'password': password}

    response = requests.post(url, data=payload)
    assert response.status_code == 200, f"Unexpected status: {response.status_code}"
    assert response.json() == {"email": email, "message": "user created"}

    # Test registering the same email again
    response = requests.post(url, data=payload)
    assert response.status_code == 400, f"Unexpected status: {response.status_code}"
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test login with incorrect password.

    Verifies that authentication fails with a 401 status code.
    """
    url = f"{BASE_URL}/sessions"
    payload = {'email': email, 'password': password}

    response = requests.post(url, data=payload)
    assert response.status_code == 401, f"Unexpected status: {response.status_code}"


def log_in(email: str, password: str) -> Optional[str]:
    """
    Test user login.

    Ensures successful login and returns the session ID.
    """
    url = f"{BASE_URL}/sessions"
    payload = {'email': email, 'password': password}

    response = requests.post(url, data=payload)
    assert response.status_code == 200, f"Unexpected status: {response.status_code}"
    assert response.json() == {"email": email, "message": "logged in"}

    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Test profile access without authentication.

    Ensures that accessing the profile endpoint without being logged in is forbidden.
    """
    url = f"{BASE_URL}/profile"

    response = requests.get(url)
    assert response.status_code == 403, f"Unexpected status: {response.status_code}"


def profile_logged(session_id: str) -> None:
    """
    Test profile access while authenticated.

    Verifies that the profile endpoint returns the user's email when logged in.
    """
    url = f"{BASE_URL}/profile"
    cookies = {'session_id': session_id}

    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200, f"Unexpected status: {response.status_code}"
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    Test user logout.

    Verifies that the session is terminated and a logout message is returned.
    """
    url = f"{BASE_URL}/sessions"
    cookies = {'session_id': session_id}

    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200, f"Unexpected status: {response.status_code}"
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Test password reset token generation.

    Ensures that a reset token is generated for the specified email.
    """
    url = f"{BASE_URL}/reset_password"
    payload = {'email': email}

    response = requests.post(url, data=payload)
    assert response.status_code == 200, f"Unexpected status: {response.status_code}"
    assert response.json()["email"] == email
    assert "reset_token" in response.json()

    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test updating the user's password.

    Ensures the password is updated using a valid reset token.
    """
    url = f"{BASE_URL}/reset_password"
    payload = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }

    response = requests.put(url, data=payload)
    assert response.status_code == 200, f"Unexpected status: {response.status_code}"
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    # Execute tests in sequence
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

