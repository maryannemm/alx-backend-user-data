#!/usr/bin/env python3
"""
This module manages interactions with the database for user-related operations.
It defines a `DB` class to handle adding, retrieving, and updating user records.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import TypeVar

VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """
    The `DB` class provides methods to interact with a user database.
    It supports creating new users, retrieving existing users, and updating user records.
    """

    def __init__(self) -> None:
        """
        Initializes the database connection and sets up the schema.
        Drops all existing tables and creates new ones for a clean state.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Provides a session object to interact with the database.
        The session is memoized for reuse within the same instance.
        Returns:
            A `Session` object bound to the database engine.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user record to the database.
        Args:
            email: The email address of the user.
            hashed_password: The hashed version of the user's password.
        Returns:
            The newly created `User` object.
        """
        if not email or not hashed_password:
            return None
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database based on specified fields.
        Args:
            **kwargs: Key-value pairs to filter the search query.
        Returns:
            The `User` object that matches the query criteria.
        Raises:
            InvalidRequestError: If any of the provided fields are invalid.
            NoResultFound: If no user matches the query criteria.
        """
        if not kwargs or any(key not in VALID_FIELDS for key in kwargs):
            raise InvalidRequestError("Invalid query field(s) provided.")
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound("No user found matching the provided criteria.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates attributes of an existing user in the database.
        Args:
            user_id: The ID of the user to update.
            **kwargs: Key-value pairs of attributes to update.
        Raises:
            ValueError: If any of the provided fields are invalid.
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in VALID_FIELDS:
                raise ValueError(f"Invalid field: {key}")
            setattr(user, key, value)
        session.commit()

