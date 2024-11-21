#!/usr/bin/env python3
"""
This module provides tools for handling user authentication, including password
hashing, user registration, session management, and password reset functionality.
"""

from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import TypeVar


def _hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.
    Args:
        password: The plain text password to be hashed.
    Returns:
        A hashed password as a string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a unique identifier (UUID).
    Returns:
        A string representation of a UUID.
    """
    return str(uuid4())


class Auth:
    """
    The Auth class interacts with the database to manage user authentication.
    It supports user registration, login, session management, and password resets.
    """

    def __init__(self):
        """
        Initializes the Auth instance and sets up the database connection.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with an email and hashed password.
        Args:
            email: The user's email address.
            password: The user's plain text password.
        Returns:
            The newly created User object.
        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user credentials.
        Args:
            email: The user's email address.
            password: The user's plain text password.
        Returns:
            True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user.
        Args:
            email: The user's email address.
        Returns:
            The session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sess_id)
            return sess_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Retrieves the email of the user associated with a session ID.
        Args:
            session_id: The session ID of the user.
        Returns:
            The user's email address or None if no user is found.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Ends the user's session by clearing the session ID.
        Args:
            user_id: The ID of the user whose session is to be destroyed.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for a user.
        Args:
            email: The user's email address.
        Returns:
            A reset token as a string.
        Raises:
            ValueError: If no user with the given email exists.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates the user's password using a reset token.
        Args:
            reset_token: The token provided for resetting the password.
            password: The new password to be set.
        Raises:
            ValueError: If the reset token is invalid or expired.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError

# # Example usage of the _hash_password function
# if __name__ == "__main__":
#     password = "Hello Holberton"
#     hashed_password = _hash_password(password)
#     print(hashed_password)

