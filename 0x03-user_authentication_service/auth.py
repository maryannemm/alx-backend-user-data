#!/usr/bin/env python3
"""
Authentication module
"""
import uuid
from bcrypt import hashpw, gensalt, checkpw
from typing import Union
from db import DB
from user import User


class Auth:
    """Auth class for handling authentication."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def _generate_uuid(self) -> str:
        """Generate a new UUID string."""
        return str(uuid.uuid4())

    def register_user(self, email: str, password: str) -> User:
        """Register a new user."""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password)
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login."""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))
        except Exception:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """Create a new session ID for a user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieve user based on session ID."""
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user's session."""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for a user."""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError("User not found")

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user's password using reset token."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = self._hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
        except Exception:
            raise ValueError("Invalid reset token")

