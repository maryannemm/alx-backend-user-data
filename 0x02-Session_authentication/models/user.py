#!/usr/bin/env python3
"""
User model for handling user data.
"""
from typing import List
import hashlib


class User:
    """Simple User class to simulate a User model."""
    users = []

    def __init__(self, email=None, password=None):
        self.email = email
        self._password = password

    @property
    def password(self):
        """Get the hashed password."""
        return self._password

    @password.setter
    def password(self, pwd: str):
        """Hash the password before storing it."""
        self._password = hashlib.md5(pwd.encode()).hexdigest()

    def is_valid_password(self, pwd: str) -> bool:
        """Check if the password is valid."""
        return hashlib.md5(pwd.encode()).hexdigest() == self.password

    def display_name(self) -> str:
        """Return the user's display name."""
        return f"{self.email}"

    def save(self):
        """Simulate saving a user to a database."""
        User.users.append(self)

    @classmethod
    def search(cls, criteria: dict) -> List['User']:
        """Search for users based on criteria."""
        return [user for user in cls.users if user.email == criteria.get('email')]

