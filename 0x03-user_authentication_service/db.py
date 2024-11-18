#!/usr/bin/env python3
"""
Database module for user authentication.
This module defines a `DB` class to interact with a database using SQLAlchemy.
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from typing import TypeVar

Base = declarative_base()

class User(Base):
    """
    User class for representing a user in the database.
    Attributes:
        id: The unique identifier for the user.
        email: The user's email address.
        hashed_password: The hashed password of the user.
        session_id: The session ID associated with the user (optional).
        reset_token: The reset token for password recovery (optional).
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


class DB:
    """
    Database class for interacting with the User table.
    This class provides methods to add, retrieve, and update users in the database.
    """
    def __init__(self):
        """
        Initialize the database connection and session.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self._engine)
        self._session = sessionmaker(bind=self._engine)

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.
        Args:
            email (str): The email address of the user.
            hashed_password (str): The hashed password of the user.
        Returns:
            User: The created User object.
        """
        session: Session = self._session()
        try:
            user = User(email=email, hashed_password=hashed_password)
            session.add(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database by arbitrary attributes.
        Args:
            kwargs: Arbitrary keyword arguments to filter users.
        Returns:
            User: The found User object.
        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If the query is invalid.
        """
        session: Session = self._session()
        try:
            return session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the given attributes")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query")
        finally:
            session.close()

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes in the database.
        Args:
            user_id (int): The ID of the user to update.
            kwargs: The attributes to update.
        Raises:
            ValueError: If an attribute in kwargs is not valid for the User model.
        """
        session: Session = self._session()
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError(f"Attribute {key} does not exist on User")
                setattr(user, key, value)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

