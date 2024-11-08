#!/usr/bin/env python3
"""
Module for encrypting passwords
"""
import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    
    :param password: Password string to hash.
    :return: Hashed password in bytes.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against the hashed version.
    
    :param hashed_password: Hashed password in bytes.
    :param password: Plain text password to validate.
    :return: True if valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

